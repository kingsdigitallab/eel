-- python manage.py syncdb will return a sql insert error because the name of the tables are too long
-- for the fields in auth_permission.
-- So we extend their lengths. 
alter table auth_permission modify column name varchar(150) NOT NULL;
alter table auth_permission modify column codename varchar(200) NOT NULL;
