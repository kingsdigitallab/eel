from .lcl import *  # noqa

set_default_db('dev', globals())

DB_MAINTENANCE = False
FRONTEND_MAINTENANCE = False
UGC_ENABLED = True
enable_ldap(globals())

EEL_IMAGE_BASE_URL = r'i/projects/eel'
IMAGE_SERVER_URL = '//loris.kdl.kcl.ac.uk/'

EMAIL_HOST = 'smtp.kcl.ac.uk'
EMAIL_PORT = 25
