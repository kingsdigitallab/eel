update editions_language set id = id + 102;
update editions_language set id = id - 100;

insert editions_language (id, name) values (1, '{unspecified}');
insert editions_language (id, name) values (2, '{unknown}');

update editions_bibliographic_entry set language_id = language_id + 2;
