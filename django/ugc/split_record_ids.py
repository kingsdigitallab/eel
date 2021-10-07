'''

Oct 2017:

Read introduction below first.

During maintenance of the project in Oct 2017, we have moved the database from
MySQL to PostgreSQL. This means that we no longer need to worry about InnoDB vs
MyISAM. And postgresql sequences are the perfect and most natural instruments to
split the ranges of record ids.

Also the last version of the project used Whoosh instead of MySQL full text
searches. So we don't have to worry about that part either.

Overall this simplifies the code a lot. All we do here is to raise an exception
if a new record ID doesn't belong to the right range of IDs.

---

Authors, Texts, Works, Productions and Text Samples can be created by editors
on the staging server, or by the registered users on the live server.

Here we split the range of available record ids in two make sure no record
created on one side has the same id as record on the other.
The lower range for staging server, higher range for live server.

To complicate matters, generating the id MUST be done in a critical section
otherwise two things can happen:
1. concurrent write will overwrite the record (same ID)
2. concurrent write will generate a DB error because the primary key is already
in use

Simplest solution is to use a standard database transaction with a high
isolation level (as we don't want any dirty read).
However, Works and Person tables have full text indices.
Which means that they must have the MyIsam engine (rather than the InnoDB).

GN: update Oct 2017, since MySQL 5.16 InnoDB (default) supports full text search.
MyIsam engine does not allow transaction.

So we force the critical section manually at the table level by surrounding
the model.save() operation with Mysql (UN)LOCK TABLES commands.

Note the important difference with a transaction: if something went wrong, it is
not rolled back.  But that's standard Django behaviour anyway.
'''

from django.conf import settings

# force all model.save() to be executed within a transaction
from django.db.models import Model
from django.db.transaction import commit_on_success
from django.db.models.fields import AutoField
from django.db import router

excluded_models = ['cms', 'picture', 'link', 'text']

model_save_base = Model.save_base

# Override model.save() only to check that the record id is within the
# band specified for that database (see databases.py)


def save_base(self, raw=False, cls=None, origin=None, force_insert=False,
              force_update=False, using=None):

    using = using or router.db_for_write(self.__class__, instance=self)

    @commit_on_success(using=using)
    def save(self, **kwargs):
        is_new_record = self.pk is None
        model_save_base(self, **kwargs)
        if isinstance(self._meta.pk, AutoField) and is_new_record:
            id_range = get_id_range_from_db_alias(using)
            if self.pk and (self.pk < id_range[0] or self.pk > id_range[1]):
                raise Exception(
                    'ERROR: EEL-ID-RANGE save() with pk in wrong id range (table: %s, id: %s)' % (self._meta.db_table, self.pk))

    save(self, raw=raw, cls=cls, origin=origin, force_insert=force_insert,
         force_update=force_update, using=using)


if Model.save_base != save_base:
    Model.save_base = save_base


def get_id_range_from_db_alias(db_alias='default'):
    '''
    Returns the range of record ids allowed for the given database.
    [ID_MIN, ID_MAX]
    '''
    db = settings.DATABASES[db_alias]

    band_size = settings.ID_RANGE_SIZE
    band_idx = db['ID_RANGE_IDX']

    return [
        (band_idx * band_size) + 1,
        ((band_idx + 1) * band_size)
    ]
