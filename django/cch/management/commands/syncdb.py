"""
Overridden syncdb command

We override South syncdb.
South syncdb will try to connect to all the entries in settings.DATABASES
Even remote ones or temporary, not yet installed databases.
So syncdb will crash because we have the full list of DBs there and some
legacy ones.

This command will just remove all other DBs than the default one before
executing South syncdb.
"""

from south.management.commands import syncdb


class Command(syncdb.Command):

    def handle_noargs(self, *args, **kwargs):
        from south.db import dbs

        # we only leave the default database for South
        for k in list(dbs.keys()):
            if k != 'default':
                del dbs[k]

        return super(Command, self).handle_noargs(*args, **kwargs)
