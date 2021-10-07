# -*- coding: utf-8 -*-
#
# Database migration script
#
# It migrates the data from the live server to the staging
# and from the staging to the live server.
#
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Manage user generated content'
    args = 'resetids'

    requires_model_validation = False

    def handle(self, *args, **options):
        # refresh the internal ordering for the folio images: filenames and
        # actual folio ordering
        if 'resetids' in args:
            fix_sequences()


def fix_sequences(db_alias='default', silent=False):
    from ugc.split_record_ids import get_id_range_from_db_alias

    id_range = get_id_range_from_db_alias(db_alias)

    ret = 0

    from django.db import connections
    from django.conf import settings
    db_settings = settings.DATABASES[db_alias]

    print('Database: %s, range %s' % (db_settings['NAME'], id_range))

    connection = connections[db_alias]
    cursor = connection.cursor()

    select_seq_info = ur'''
        select table_name, column_name
        from information_schema.columns
        where table_catalog = %s
        and column_default like %s
        order by table_name
    '''

    cur = sql_select(
        connection, select_seq_info, [
            db_settings['NAME'], ur'nextval%'])

    while True:
        rec = cur.fetchone()
        if not rec:
            break
        params = {
            'table_name': rec[0],
            'seq_field': rec[1],
            'seq_value': max(sql_select_max_value(connection, rec[0], rec[1], id_range), id_range[0])
        }

        if not silent:
            print '%8s %s.%s' % (params['seq_value'], params['table_name'], params['seq_field'])
        cmd = "select setval('%(table_name)s_%(seq_field)s_seq', %(seq_value)s )" % params
        cursor.execute(cmd)
        ret += 1
    cur.close()
    cursor.close()

    return ret


def sql_select(con, command, arguments=[]):
    ''' return a cursor,
        caller need to call .close() on the returned cursor
    '''
    cur = con.cursor()
    cur.execute(command, arguments)

    return cur


def sql_select_max_value(con, table, field, id_range):
    ret = id_range[0]
    cur = sql_select(con, 'select max(%s) from %s where %s between %s AND %s' % (
        field, table, field, id_range[0], id_range[1]))
    rec = cur.fetchone()
    if rec and rec[0]:
        ret = rec[0]
    cur.close()

    return ret
