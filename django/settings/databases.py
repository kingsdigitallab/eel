DATABASES = {
    # local machine
    'lcl': {
        'NAME': 'eel',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER': 'eel',
        'PASSWORD': 'eel',
        'PORT': '5432',
        'HOST': 'rdbms',
        'OPTIONS': {},
        'TIME_ZONE': 'Europe/London',
        'ID_RANGE_IDX': 0,
        'DEBUG': True,
    },
}
