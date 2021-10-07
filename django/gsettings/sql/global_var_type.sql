insert into gsettings_global_var_type (id, name) values (1, 'string');
insert into gsettings_global_var_type (id, name) values (2, 'int');
insert into gsettings_global_var_type (id, name) values (3, 'float');
insert into gsettings_global_var_type (id, name) values (4, 'datetime');
insert into gsettings_global_var_type (id, name) values (5, 'date');

insert into gsettings_global_var_category (id, name, description) values (1, 'General', 'General category');

-- for testing only...
insert into gsettings_global_var (id, name, label, value, global_var_category_id, global_var_type_id, description, unit) values (1, 'n1', 'Variable 1', 'v1', 1, 1, '', '');
insert into gsettings_global_var (id, name, label, value, global_var_category_id, global_var_type_id, description, unit) values (2, 'n2', 'Variable Two', '2', 1, 2, '', '');
insert into gsettings_global_var (id, name, label, value, global_var_category_id, global_var_type_id, description, unit) values (3, 'n3', 'Variable Three', '2010-08-10 21:02:00', 1, 4, '', '');
