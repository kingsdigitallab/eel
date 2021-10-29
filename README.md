# Early English Laws (EEL)

This repository contains a copy of the legacy code of the Early English Laws web application, developed by G. Noel at DDH (2009-2012), King's College London.

## Stack

* Web framework: Django & DjangoCMS
* Search: Whoosh
* Database: postgresql
* Image server: IIIF, such as Loris
* Python: 2.7
* OS: Ubuntu 16.04

## Repository

### /django

The /django folder contains the code of the django project and custom-built django apps / packages.

* settings: the settings for the django project
* editions: the editions data models, logic, controllers and web views
* convert_data: django command line tools to import and pre/post-process various type of content (images, bibliography, diagrams, HTML of the editions)
* templates: the Django templates for the front- & back-end pages of the site

Less edition-specific:

* ugc: app to manage user generated content on the frontend
* cch: generic toolbox of helpers for the other apps
* graphlayout: generate the SVG of the edition diagrams
* gsettings: some django manage project settings from the admin interface and store them in the DB  
* pagination: a web result pagination helper
* registration: manage public user sign up, log ins and profiles
* simplejson: third-party package to handle json data structure
* uml2django: UML to django models conversion tool

### /doc

The /doc folder contains supporting documentation and sample content

* eel-liv-schema-20211022-psql.sql: a dump of the database schema

Early logical diagram of the schema:
![diag](https://github.com/kingsdigitallab/eel/raw/main/django/models/editions-logical.png)


## Running the web application

Make sure Docker is installed on the machine.

Unzip the database

`unzip build/rdbms/dbs/eel-liv-sample.psql.sql.zip -d build/rdbms`

Run the following command from the terminal:

`docker-compose -f build/compose.yaml up`

Re-index the search engine:

`docker-compose -f build/compose.yaml exec django python manage.py txtidx`

Visit the site at http://localhost:9083/ 
Backend admin interface at /admin (user admin, password on request)

