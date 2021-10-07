#!/bin/bash
cd /eel/stg/website/django/eel
python manage.py eelmigrate > migrate/migrate.log
