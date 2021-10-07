INSERT INTO `editions_collection_of_editions` (`id`, `name`, `eel_project`) VALUES (1,'Early English Law Project',1),(2,'Die Gesetze der Angelsachsen',0);

-- edition status (used by work)

INSERT INTO `editions_eel_edition_status` (`id`, `name`) VALUES (1,'Edition Accepted'),(2,'Proposal in process');

-- editor (used by work)

INSERT INTO `editions_editor` (`id`, `name`) VALUES (1,'Bruce O\'Brien');

-- edition of a work

INSERT INTO `editions_edition_of_a_work` (`id`, `abbreviation`, `introduction`, `date_of_edition_to`, `date_of_edition_mod`, `date_of_edition`, `work_id`, `collection_of_editions_id`, `eel_edition_status_id`) VALUES (1,'GPKP','',NULL,0,NULL,1,2,2);

