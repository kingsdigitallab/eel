# -*- coding: utf-8 -*-
#
# Database migration script
#
# It migrates the data from the live server to the staging
# and from the staging to the live server.
#
from django.core.management.base import BaseCommand
from django.db.models.fields.related import RelatedField
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError
import re
from ugc.split_record_ids import get_id_range_from_db_alias
from optparse import make_option
from django.db.models.fields import DateField
from django.db.models.fields.files import FieldFile


class InvalidForeignKey(Exception):
    '''A foreign key points to an record which does not exists in the destination database'''
    pass

# TODO:
# deal with removals!
# deal with generic relationships (ordering tables. E.g. make sure
# user_submission is after work, author and text)


class Command(BaseCommand):
    help = 'Synchronise the back and front end databases.'
    #args = '[appname ...]'
    args = ''

    option_list = BaseCommand.option_list + (
        make_option('--dry-run', action='store_true',
                    help='Read only, database will not be modified'),
        make_option('--no-sort-order', action='store_true',
                    help='Don\'t reset sort order', dest='no_sort_order'),
    )

    requires_model_validation = False

    def print_help(self, *args, **kwargs):
        ret = super(Command, self).print_help(*args, **kwargs)

        print
        print self.get_sync_desc()
        print

        return ret

    def get_sync_desc(self):
        ret = '%s (Back) <-> %s (Front) (See settings.EEL_MIGRATE_ALIASES)' % (
            self.backend,
            self.frontend
        )
        return ret

    def __init__(self):
        self.connections = {}
        self.instance_reprs = {}
        self.read_only = True
        from django.conf import settings
        self.setConnections(*settings.EEL_MIGRATE_ALIASES)
        self.setLogLevel(2)

    def setConnections(self, backend_server_name, frontend_server_name):
        self.backend = backend_server_name
        self.frontend = frontend_server_name

    def handle(self, *args, **options):
        # refresh the internal ordering for the folio images: filenames and
        # actual folio ordering
        self.options = options
        self.read_only = options['dry_run']
        self.setLogLevel(int(options['verbosity']) + 1)

        action = args[0] if args else 'help'

        knwon_command = False

        if action == 'sync':
            print self.get_sync_desc()

            knwon_command = True

            from editions.models import Folio_Image
            images = Folio_Image.objects
            if not self.options['no_sort_order']:
                self.log('reset Folio_Image.filename_sort order', 2)
                images.bulkNaturalFileNameSortOrder(using=self.backend)
                self.log('reset Folio_Image.display_sort order', 2)
                images.bulkNaturalDisplayOrderSorting(using=self.backend)

            self.synchronise()
            # self.intialiseFrontEnd()

            self.log('ALL DONE', 2)

        if not knwon_command:
            this_command_name = re.sub(ur'.*?(\w+)\.py', ur'\1', __file__)
            self.print_help(this_command_name, 'sync')

    def intialiseFrontEnd(self):
        ''' Only need to be called once to initialise the data on the live server '''
        app_prefixes = [
            'gsettings',
        ]
        models = [ct.model_class()
                  for ct in ContentType.objects.filter(app_label__in=app_prefixes)]
        models, missing, expanded = self.orderModels(models, True)
        self.migrate(self.backend,
                     self.frontend, models, False, True)

    def synchronise(self):
        self.log('Start synchronisation.', 2)
        if self.read_only:
            self.log('READ ONLY MODE', 1)
        # The order is crucial here.
        # If we do the opposite order, the moderation of the comments will be
        # undone.
        self.synchroniseBackToFront()
        self.synchroniseFrontToBack()

        read_only = ''
        if self.read_only:
            read_only = '(READ ONLY MODE)'
        self.log('End Synchronisation %s' % read_only, 2)

    def synchroniseBackToFront(self):
        self.log('##################', 2)
        self.log('#  BACK -> FRONT #', 2)
        self.log('##################', 2)

        # NOTE: the following settings has been carefully configured
        # please make sure you fully understand why some models are inluded or not
        # before making any change
        app_prefixes = [
            #'ugc',  # web users and directories, see below for fine-grained migration
            #'user_tags', # see below for fine-grained migration

            'editions',
            #'version',
            #'admin', # log_entry / admin_log
            #'comments_section',
        ]

        from editions import models as edition_models

        model_names = '''
        Bibliographic_Entry_Bib_Category,
        Folio_Image,
        Version_Witness,
        Witness_Language,
        Edition,
        User_Comment,
        Commentary,
        Hyparchetype,
        Text_Attribute_Work,
        Glossary_Term,
        Resource,
        Topic,
        Place,
        Version_Relationship,
        Editor_Edition,
        Version_Language,
        '''

        models = [
            getattr(edition_models, model_name)
            for model_name
            in re.findall(ur'\w+', model_names)
        ]

        models, missing, expanded = self.orderModels(models, True)

        models.append(ContentType)

        # print '\n'.join([m.__name__ for m in models])

        self.migrate(
            self.backend,
            self.frontend,
            models,
            all_id_ranges=True,
            can_delete=False
        )

    def synchroniseFrontToBack(self):
        self.log('##################', 2)
        self.log('#  BACK <- FRONT #', 2)
        self.log('##################', 2)
        from editions.models import User_Comment
        from django.contrib.auth.models import User
        from ugc.models import Web_User_User_Directory, User_Directory, Web_User
        # 2. liv -> stg
        # NOTE: the following settings has been carefully configured
        # please make sure you fully understand why some models are inluded or not
        # before making any change

        #models = [ct.model_class() for ct in ContentType.objects.filter(app_label__in=app_prefixes)]
        models = [User, User_Comment, Web_User_User_Directory]
        #models = [User]
        models, missing, expanded = self.orderModels(models, True)

        self.migrate(
            self.frontend,
            self.backend,
            models,
            all_id_ranges=False,
            can_delete=False
        )

    def migrate(self, source, destination,
                models, all_id_ranges=False, can_delete=False):
        record_count = 0
        for model in models:
            record_count += self.migrateTable(
                model,
                source,
                destination,
                all_id_ranges, can_delete
            )
        self.log('MIGRATION FINISHED (%d record(s))' % record_count, 2)

    def migrateTable(self, model, source, destination,
                     all_id_ranges=False, can_delete=False):
        # TODO: this function should return a generator instead of a list with all the records.
        # can be very expensive in memory
        self.log('TABLE %s / %s' % (model.__name__, model._meta.db_table), 2)
        records = self.getRecordsFromTable(model, source, all_id_ranges)
        # print records
        change_counts = [0, 0, 0, 0]

        for record_array in records:
            # set the destination record
            change_type = self.saveRecordArray(
                model, record_array, source, destination)
            change_counts[change_type] += 1

        if can_delete:
            change_counts[3] = self.deleteRecords(model, records, destination)

        self.log(
            '  %7d Cr |%7d Re |%7d Up |%7d De |%7d Sk |%7d Total' % (
                change_counts[2], len(records),
                change_counts[1], change_counts[3],
                change_counts[0],
                change_counts[1] + change_counts[2] + change_counts[3]
            ),
            2
        )

        return change_counts[1] + change_counts[2]

    def deleteRecords(self, model, records, destination):
        # returns number of deleted records
        # 1. check if the record already exists
        pk_name = model._meta.pk.attname
        table_name = model._meta.db_table

        # self.log('\t%s - #%s' % (table_name, record_array[pk_name]), 3)
        if len(records):
            sql_from_where = 'FROM %s WHERE %s NOT IN (%s)' % (
                table_name, pk_name, ', '.join([str(record[pk_name]) for record in records]))
        else:
            sql_from_where = 'FROM %s' % table_name

        # find the number of records that will be deleted
        cursor_select = self.executeSql(
            "SELECT count(*) %s " % sql_from_where, destination)
        ret = cursor_select.fetchone()
        ret = ret[0]

        # actually delete the records
        if not self.read_only:
            cursor_select = self.executeSql(
                "DELETE  %s " % sql_from_where, destination)
            cursor_select.close()

        return ret

    def getRecordsFromTable(self, model, db_alias, all_id_ranges=False):
        id_range = get_id_range_from_db_alias(db_alias)

        recs = model.objects.using(db_alias).all()
        if not all_id_ranges:
            recs = recs.filter(pk__range=id_range)
        recs = recs.order_by('id')

        ret = []
        for rec in recs:
            # print rec.pk, id_range[0], id_range[1], getattr(rec,
            # 'last_login', None)

            rec_array = {}
            for field in model._meta.fields:
                rec_array[field.attname] = getattr(rec, field.attname)

            if rec_array is not None:
                ret.append(rec_array)

        return ret

    def saveRecordArray(self, model, record_array, source, destination):
        # returns 1 for update, 2 for insert and 0 for nothing
        # This record may be stored in more than one table due to model inheritance.
        # This function detects inheritance and split the record array in two record arrays, one for each individual model
        # The following algorithm supports only one level of inheritance
        from django.db import models

        for cls in model.__bases__:
            if issubclass(
                    cls, models.Model) and cls != models.Model and not cls._meta.abstract:
                record_array_base = {}
                for field in cls._meta.fields:
                    if field.attname in record_array:
                        record_array_base[field.attname] = record_array[field.attname]
                        record_array.pop(field.attname)
                if len(record_array_base):
                    self.saveRecordArraySingleModel(
                        cls, record_array_base, source, destination)

        # we silently remove unknown fields
        field_names = record_array.keys()
        for field_name in field_names:
            field = self.getModelFieldByAttname(model, field_name)
            if field is None:
                record_array.pop(field_name)
                self.log('unknown field %s.%s' %
                         (model.__name__, field_name), 1)

        return self.saveRecordArraySingleModel(
            model, record_array, source, destination)

    def saveRecordArraySingleModel(
            self, model, record_array, source, destination):
        # returns 1 for update, 2 for insert and 0 for nothing
        ret = 0
        # 1. check if the record already exists
        pk_name = model._meta.pk.attname
        table_name = model._meta.db_table
        from django.contrib.comments import Comment

        self.log('\t%s - #%s' % (table_name, record_array[pk_name]), 3)

        cursor_select = self.executeSql("SELECT %s FROM %s WHERE %s = %s" % (
            pk_name, table_name, pk_name, record_array[pk_name]), destination)
        row = cursor_select.fetchone()
        command = ''
        values = []
        try:
            if row is None:
                # insert
                field_names = ''
                value_subs = ''
                for key in record_array:
                    if len(field_names) > 0:
                        field_names = field_names + ', '
                        value_subs = value_subs + ', '
                    #field_names = field_names + self.getColumnNameFromFieldName(model, key)
                    field_names = field_names + key
                    value_subs = value_subs + '%s'
                    values.append(self.getDBValueFromModelValue(
                        model, key, record_array, source, destination))
                command = '''INSERT INTO %s
                                (%s) VALUES (%s);
                            ''' % (table_name, field_names, value_subs)
                ret = 2
            else:
                # update
                assignments = ''
                for key in record_array:
                    if len(assignments) > 0:
                        assignments = assignments + ', '
                    #assignments = assignments + self.getColumnNameFromFieldName(model, key) + ' = %s'
                    assignments = assignments + key + ' = %s'
                    values.append(self.getDBValueFromModelValue(
                        model, key, record_array, source, destination))
                command = '''UPDATE %s
                                SET %s
                            WHERE %s = %s
                            ''' % (table_name, assignments, pk_name, record_array[pk_name])
                ret = 1
            if not self.read_only:
                cursor_save = self.executeSql(command, destination, values)
                cursor_save.close()
        except InvalidForeignKey:
            pass

        cursor_select.close()

        return ret

    #---------------------------------------
    #            DATABASE UTILITIES
    #---------------------------------------

    def getDBValueFromModelValue(self, model, field_name, record_array,
                                 source, destination):
        ''' The value in the model can be different from the value in the database.
            e.g. language = Spanish, corresponds to language_id = 3
        '''

        value = record_array[field_name]
        ret = value
        field = self.getModelFieldByAttname(model, field_name)
        self.log(u'\t\t%s (%s) = %s (%s)' %
                 (field_name, type(field), repr(value), type(value)), 3)

        # NONE
        if value is None or value == u'None':
            # print '%s, %s , %s' % (value, model.__name__, field_name)
            if value == u'None' and\
                ((model.__name__ == 'Courtesy_Title' and field_name == 'name')
                 or (model.__name__ == 'LogEntry' and field_name == 'object_repr')):
                ret = 'None'
            else:
                ret = None
        else:
            # DATES
            from cch.fuzzydate.fields import FuzzyDate, FuzzyDateField
            if isinstance(value, FuzzyDate) and value.ukFormat:
                # print 'FUZZYDATE'
                date = value.getDateFrom()
                ret = '%4d-%02d-%02d' % (date.year, date.month, date.day)
            elif isinstance(field, FuzzyDateField):
                date = FuzzyDate()
                date.setAsString(value)
                date = date.getDateFrom()
                ret = '%4d-%02d-%02d' % (date.year, date.month, date.day)
                # print 'FUZZYDATEFIELD CORRECTION %s' % ret
            elif isinstance(field, DateField) and isinstance(value, basestring):
                # date elements might have been saved in the wrong
                # order
                ret = re.sub(r'^(\d\d)-(\d\d)-(\d\d\d\d)$', r'\3-\2-\1', value)
                # print 'DATE CORRECTION %s' % ret

            if isinstance(value, FieldFile):
                ret = ur'%s' % value

            # RELATED FIELDS
            if issubclass(field.__class__, RelatedField):
                rel_model = field.rel.to
                # check if the related record exists
                recs_qs = rel_model.objects.using(destination).filter(id=value)
                if recs_qs.count() == 0:
                    action_str = ''
                    if field.null:
                        action_str = 'set FK to NULL'
                        ret = None
                    else:
                        action_str = 'record NOT written'
                    error_message = u'Foreign key points to a record that does not exist (%s.%s = %s) - %s' % (
                        model.__name__, field_name, value, action_str)
                    self.log(error_message, 1)
                    if not field.null:
                        raise InvalidForeignKey(error_message)

        return ret

    def getModelFromContentTypeID(self, ctid):
        return ContentType.objects.get(id=ctid).model_class()

    def getModelFieldByAttname(self, model, attname):
        ret = None
        for field in model._meta.fields:
            if field.attname == attname:
                ret = field
                break
        return ret

    def getColumnNameFromFieldName(self, model, field_name):
        return model._meta.get_field_by_name(field_name)[0].attname

    def executeSql(self, command, db_alias, arguments=[]):
        ''' return a cursor,
            caller need to call .close() on the returned cursor
        '''
        self.log(u'\t%s (%s)' % (command, db_alias), 3)
        from django.db import connections, transaction
        ret = connections[db_alias].cursor()
        try:
            res = ret.execute(command, arguments)
            transaction.commit_unless_managed(using=db_alias)
        except IntegrityError as e:
            self.log(u'SQL Error: %s - SQL: %s' % (e, command), 1)
        return ret

    def orderModels(self, seed, can_expand=False):
        ''' OUT:
                This function sort the tables in the seed by dependency.
                Placing first the tables which have no foreign keys to other tables.
                It returns a list made of three items:
                    * a list is the ordered models
                        Should always contain at least all the tables from [seed]
                    * a list of missing models (i.e. a table which was not in seed but referenced by a table from seed).
                        Always empty if can_expand = True
                    * a list of models added to the seed (see [can_expand])
                        Always empty is can_expand = False
            IN:
                [Seed] is a list of models
                [can_expand] if True, the seed is expanded with tables referenced by the seed
                    but not initially in the seed.
        '''
        tables = []
        expansion = []
        missing_tables = []
        missing_tables_old = seed
        while len(missing_tables_old) > 0:
            missing_tables = []
            for model in seed:
                if model in tables:
                    continue
                if True:
                    i = 0
                    # True if all the dependencies have been resolved
                    resolved = True
                    for field in model._meta.fields:
                        i = i + 1
                        rel_model = None
                        if issubclass(field.__class__, RelatedField):
                            rel_model = field.rel.to
                        if rel_model is not None and rel_model != model and rel_model not in tables:
                            try:
                                missing_tables.index(rel_model)
                            except Exception:
                                missing_tables.append(rel_model)
                            resolved = False
                        else:
                            rel_model = None
                    if resolved:
                        tables.append(model)

            if missing_tables_old == missing_tables:
                if can_expand:
                    # move all the missing tables to [tables] and [expansion]
                    # TODO: circular dependencies in can_expand mode will lead
                    # to infinite loops
                    for model in missing_tables:
                        if model not in seed:
                            seed.append(model)
                            expansion.append(model)
                else:
                    # append all the tables from the seed which dependencies haven't been resolved
                    # either because the related table is not in the seed
                    # or because of circular dependencies
                    for model in seed:
                        if model not in tables:
                            tables.append(model)
                    break
            missing_tables_old = missing_tables

        return (tables, missing_tables, expansion)

    def setLogLevel(self, log_level=1):
        self.log_level = log_level

    def log(self, message, log_level=3):
        ''' log_level:
                0: fatal error
                1: warning
                2: info
                3: debug
        '''
        if log_level <= self.log_level:
            prefixes = ['ERROR: ', 'WARNING: ', '', '']
            from datetime import datetime
            timestamp = datetime.now().strftime("%y-%m-%d %H:%M:%S")
            try:
                print u'[%s] %s%s' % (timestamp, prefixes[log_level], message)
            except UnicodeEncodeError:
                print '???'

    def testOrderModels(self):
        from django.contrib.contenttypes.models import ContentType
        #from ootw.plays.models import Author, Author_Work, Person
        app_prefixes = ['plays']
        cts = ContentType.objects.filter(app_label__in=app_prefixes)
        a, b, c = self.orderModels([ct.model_class() for ct in cts], True)
        print a
        print '---'
        print b
        print '---'
        print c
