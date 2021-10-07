from .base import *  # noqa

DJANGO_WEBPATH_PREFIX = ''

# See databases.py
set_default_db('lcl', globals())
# The db aliases used for the data sync: [BACKEND, FRONTEND]
EEL_MIGRATE_ALIASES = ['lcl-stg', 'lcl-liv']

# Set this to True to show a maintenance message instead of the admin
# interface.
DB_MAINTENANCE = False
FRONTEND_MAINTENANCE = False
LDAP_ENABLED = False
UGC_ENABLED = True

if LDAP_ENABLED:
    enable_ldap(globals())

# EEL_IMAGE_BASE_URL = r'http://images.cch.kcl.ac.uk/eel/incoming/'
# EEL_IMAGE_BASE_URL = r'http://localhost:8000/media/website/_a/i'
# EEL_IMAGE_BASE_URL = r'file:///vol/i/projects/eel'
EEL_IMAGE_BASE_URL = r'i/projects/eel'

# DJATOKA RESOLVER
# IMAGE_SERVER_URL = '/adore-djatoka/resolver'
# IMAGE_SERVER_URL = 'http://i.cch.kcl.ac.uk/adore-djatoka/resolver'
# IMAGE_SERVER_URL = 'http://www.earlyenglishlaws.ac.uk/adore-djatoka/resolver'
IMAGE_SERVER_URL = '//loris.kdl.kcl.ac.uk/'

# DJANGO DEBUG
INTERNAL_IPS = ('127.0.0.1',)

EMAIL_HOST = 'localhost'
EMAIL_PORT = 2525

