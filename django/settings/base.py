# Django settings for ootw project.
# THIS CONFIGURATION FILE SHOULD BE THE SAME ON ALL SERVERS
# CUSTOMISATIONS SHOULD GO INTO settings_custom.py
import os

# DATABASE


def set_default_db(db_alias, settings_vars):
    gs = settings_vars
    from .databases import DATABASES
    gs['DATABASES'] = DATABASES
    #assert('default' not in DATABASES)
    DATABASES['default'] = DATABASES[db_alias]
    gs['DEBUG'] = DATABASES['default'].get('DEBUG', False)
    gs['TEMPLATE_DEBUG'] = gs['DEBUG']

# DJANGO CMS


def gettext(s): return s


# Contains the absolute path to the project directory
PROJECT_FILEPATH = os.path.normpath(
    os.path.join(os.path.dirname(__file__), '..'))

ADMINS = (
)

MANAGERS = ADMINS

# List of authentication backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]


def enable_ldap(settings_vars):
    settings_vars['AUTHENTICATION_BACKENDS'].insert(
        0, 'cch.backends.ldap_backend.LDAPBackend')


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# ---------------------------------------------------

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
#MEDIA_ROOT = ''
MEDIA_ROOT = PROJECT_FILEPATH + '/media/'
# Only used when django serves the media files (see url.py)
WEBSITE_ROOT = MEDIA_ROOT + 'website/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
# GN: IMPORTANT, it is used everywhere in the django templates and should
# be mapped to the django admin/media folder
ADMIN_MEDIA_PREFIX = '/dj_media/'

# GN, see mapping in urls.py
# used for all the custom media files (>< admin_media_prefix)
CUSTOM_MEDIA_PREFIX = '/media/'
CUSTOM_ADMIN_MEDIA_PREFIX = CUSTOM_MEDIA_PREFIX + 'admin/'
#CUSTOM_WEB_MEDIA_PREFIX = 'http://eel-local.cch.kcl.ac.uk/'
CUSTOM_WEB_MEDIA_PREFIX = CUSTOM_MEDIA_PREFIX + 'website/'


CACHE_BACKEND = 'locmem:///?max_entries=1000&timeout=1800'
ADMIN_INCLUDE_CACHE = 60 * 60 * 1

# only used in url.py?
ADMIN_INCLUDE_ROOT = PROJECT_FILEPATH + '/media/admin/'

# ---------------------------------------------------

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'l!u_v_1^7#-)+a2^lf4@r(^j##p)hquslosicw52li%-n#n@62'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    # Defined in the same ORDER Django search through them.

    # Loads templates from the filesystem, according to TEMPLATE_DIRS.
    # This loader is enabled by default.
    'django.template.loaders.filesystem.Loader',
    # Loads templates from Django apps on the filesystem.
    # For each app in INSTALLED_APPS, the loader looks for a
    # templates subdirectory.
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.load_template_source',
    # dbtemplate: for template saved in the database and edited in the admin
    #'dbtemplates.loader.load_template_source',
    #'dbtemplates.loader.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.request",
    "django.core.context_processors.media",
    "gsettings.context_processor.all_gvars",
    # DJANGO CMS
    "cms.context_processors.media",
    # this context processor adds some useful settings variables in the context
    "editions.context_processor.settings_vars",
)

ERROR_LOG_FILENANE = PROJECT_FILEPATH + '/logs/error.log'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    # CMS - next line
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # CMS - next line
    'cms.middleware.media.PlaceholderMediaMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    # CMS - next line
    'cms.middleware.user.CurrentUserMiddleware',
    #'cms.middleware.multilingual.MultilingualURLMiddleware',
    'cch.middleware.errorlog.ErrorLogMiddleware',
    # Django-pagination
    'pagination.middleware.PaginationMiddleware',
)

ROOT_URLCONF = 'eel.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJECT_FILEPATH + '/templates',
)

APPEND_SLASH = True

# ------------------
# CMS
CMS_TEMPLATES = (
    ('website/eel_default.html', gettext('eel-default')),
)

LANGUAGES = (
    #('fr', gettext('French')),
    #('de', gettext('German')),
    ('en', gettext('English')),
)

#CMS_MEDIA_PATH = CUSTOM_MEDIA_ROOT + "cms/"
#CMS_MEDIA_URL = CUSTOM_MEDIA_PREFIX + "cms/"
#CMS_MEDIA_URL = CUSTOM_MEDIA_PREFIX + "cms/"
#CMS_MEDIA_URL = CUSTOM_MEDIA_PREFIX + "cms/"

CMS_PLACEHOLDER_CONF = {
    'body': {
        "plugins": ("TextPlugin", "LinkPlugin", "FilePlugin"),
        "extra_context": {"theme": "16_5"},
        "name": gettext("body"),
    },
}

# --------------------
# LDAP configuration
# see auth/backends.py for explanation about the properties

#LDAP_SERVER_URI = 'ldap://ldap.cch.kcl.ac.uk'
LDAP_SERVER_URI = 'ldap://ldap1.cch.kcl.ac.uk'
#LDAP_SEARCHDN = 'dc=cch,dc=kcl,dc=ac,dc=uk'
LDAP_SEARCHDN = 'dc=dighum,dc=kcl,dc=ac,dc=uk'
LDAP_SEARCH_FILTER = 'uid=%s'
LDAP_UPDATE_FIELDS = True
LDAP_FIRST_NAME = 'givenName'
LDAP_LAST_NAME = 'sn'

# Optional Settings
LDAP_FULL_NAME = None
LDAP_GID = 'memberUid'
LDAP_SU_GIDS = None
#LDAP_STAFF_GIDS = ['cn=eel,dc=cch,dc=kcl,dc=ac,dc=uk']
LDAP_STAFF_GIDS = ['cn=eel,ou=groups,dc=dighum,dc=kcl,dc=ac,dc=uk']
LDAP_ACTIVE_FIELD = None
LDAP_ACTIVE = None
LDAP_EMAIL = None
LDAP_DEFAULT_EMAIL_SUFFIX = None
LDAP_OPTIONS = None
LDAP_DEFAULT_GROUP = 'editor'
LDAP_ALL_STAFF = True


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'south',
    'gsettings',
    # DB TEMPLATES
    #'dbtemplates',
    'eelmigrate',
    # Django CMS
    'cms',
    'menus',
    'cms.plugins.text',
    'cms.plugins.picture',
    'cms.plugins.link',
    'cms.plugins.file',
    #'cms.plugins.snippet',
    #'cms.plugins.googlemap',
    'mptt',
    'publisher',
    # this is only required because we need to load the template tags
    'cch',
    'editions',
    'uml2django',
    'tinymce',
    'convert_data',
    'httpproxy',
    'pagination',
    'ugc',
    'registration',
)

# --------------------
# TINYMCE

TINYMCE_JS_URL = CUSTOM_ADMIN_MEDIA_PREFIX + 'js/tiny_mce/tiny_mce.js'
TINYMCE_JS_ROOT = ADMIN_INCLUDE_ROOT + 'js/tiny_mce'
TINYMCE_COMPRESSOR = False
TINYMCE_DEFAULT_CONFIG = {
    'theme': 'advanced',
    'relative_urls': False,

    'theme_advanced_toolbar_location': 'top',
    'theme_advanced_toolbar_align': 'left',
    'theme_advanced_layout_manager': 'SimpleLayout',
    'theme_advanced_blockformats': 'h2,h3,h4,h5,h6,blockquote',
    'theme_advanced_buttons1': 'formatselect, bold,italic,bullist,numlist,removeformat,link,separator,undo,redo,separator,code',
    'theme_advanced_buttons2': 'tablecontrols',
    'theme_advanced_buttons3': '',

    'width': '100%',
    'height': '300px',

    'plugins': 'table',
    #'table_styles' : 'Header 1=header1;Header 2=header2;Header 3=header3',
    'table_row_styles': 'Odd=z02;Even=z01;Header:r01 z01',
    'table_cell_styles': 'First=c01;Last=x01',
}

# --------------------
# CMS APPs URLs

CMS_APPLICATIONS_URLS = (
    ('editions.reference_urls', 'reference'),
    ('editions.synopsis_urls', 'laws'),
    ('editions.laws_urls', 'laws'),
    ('editions.search_urls', 'laws'),
    ('ugc.urls', 'user'),
)

# --------------------
# DJANGO_REGISTRATION

DJANGO_WEBPATH_PREFIX_MEMBERS = 'user/'
ACCOUNT_ACTIVATION_DAYS = 7

# -----------------------------------------------------------------------------
# EMAIL SETTINGS
# -----------------------------------------------------------------------------

EMAIL_HOST = 'smtp.kcl.ac.uk'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
# Domain kcl.ac.uk MUST MATCH smtp server otherwise emails treated as spam
# Note that our smtp server will refuse sending from non-existent accounts
# e.g. early-english-laws-noreply, early.english.laws.noreply
DEFAULT_FROM_EMAIL = 'noreply@kcl.ac.uk'
# Sender of error messages to ADMINS and MANAGERS
SERVER_EMAIL = DEFAULT_FROM_EMAIL
EMAIL_SUBJECT_PREFIX = 'Early English Laws'

# --------------------
# PROXY

#PROXY_DOMAIN = 'localhost'
#PROXY_PORT = 8080
PROXY_DOMAIN = 'i.cch.kcl.ac.uk'
PROXY_PORT = 8182

# DO NOT CHANGE THIS VALUE!
# See eelmigrate and mugc
ID_RANGE_SIZE = 10000000

