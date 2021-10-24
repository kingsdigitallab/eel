--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.25
-- Dumped by pg_dump version 9.5.25

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE ONLY public.cms_page_placeholders DROP CONSTRAINT placeholder_id_refs_id_b0df4960;
ALTER TABLE ONLY public.cms_page_placeholders DROP CONSTRAINT page_id_refs_id_b22baae5;
ALTER TABLE ONLY public.cms_cmsplugin DROP CONSTRAINT new_placeholder_id_refs_id_df6bb944;
DROP INDEX public.idx_154085_ugc_web_user_user_directory_web_user_id;
DROP INDEX public.idx_154085_ugc_web_user_user_directory_user_directory_id;
DROP INDEX public.idx_154076_user_id;
DROP INDEX public.idx_154070_name;
DROP INDEX public.idx_154061_name;
DROP INDEX public.idx_154052_request_id;
DROP INDEX public.idx_154037_name;
DROP INDEX public.idx_154028_name;
DROP INDEX public.idx_154019_name;
DROP INDEX public.idx_154019_gsettings_global_var_global_var_type_id;
DROP INDEX public.idx_154019_gsettings_global_var_global_var_category_id;
DROP INDEX public.idx_154013_name;
DROP INDEX public.idx_154013_editions_work_king_id;
DROP INDEX public.idx_153965_name;
DROP INDEX public.idx_153956_editions_version_relationship_version_relationship_t;
DROP INDEX public.idx_153941_standard_abbreviation;
DROP INDEX public.idx_153926_name;
DROP INDEX public.idx_153920_editions_text_attribute_work_work_id;
DROP INDEX public.idx_153920_editions_text_attribute_work_text_attribute_id;
DROP INDEX public.idx_153914_name;
DROP INDEX public.idx_153908_name;
DROP INDEX public.idx_153896_name;
DROP INDEX public.idx_153890_name;
DROP INDEX public.idx_153881_shelf_mark;
DROP INDEX public.idx_153875_name;
DROP INDEX public.idx_153854_term;
DROP INDEX public.idx_153848_name;
DROP INDEX public.idx_153839_filepath;
DROP INDEX public.idx_153833_name;
DROP INDEX public.idx_153821_abbreviation;
DROP INDEX public.idx_153806_editions_edition_bibliographic_entry_edition_id;
DROP INDEX public.idx_153806_editions_edition_bibliographic_entry_bibliographic_e;
DROP INDEX public.idx_153782_name;
DROP INDEX public.idx_153776_editions_bibliographic_entry_bib_category_bibliograp;
DROP INDEX public.idx_153776_editions_bibliographic_entry_bib_category_bib_catego;
DROP INDEX public.idx_153767_editions_bibliographic_entry_language_id;
DROP INDEX public.idx_153761_cityname;
DROP INDEX public.idx_153755_template_id;
DROP INDEX public.idx_153755_site_id_refs_id_29215c49;
DROP INDEX public.idx_153746_name;
DROP INDEX public.idx_153728_app_label;
DROP INDEX public.idx_153719_django_admin_log_user_id;
DROP INDEX public.idx_153719_django_admin_log_content_type_id;
DROP INDEX public.idx_153710_cms_title_slug;
DROP INDEX public.idx_153710_cms_title_path;
DROP INDEX public.idx_153710_cms_title_page_id;
DROP INDEX public.idx_153710_cms_title_language;
DROP INDEX public.idx_153710_cms_title_has_url_overwrite;
DROP INDEX public.idx_153710_cms_title_application_urls;
DROP INDEX public.idx_153705_cms_pageusergroup_created_by_id;
DROP INDEX public.idx_153702_cms_pageuser_created_by_id;
DROP INDEX public.idx_153698_cms_pagepermission_user_id;
DROP INDEX public.idx_153698_cms_pagepermission_page_id;
DROP INDEX public.idx_153698_cms_pagepermission_group_id;
DROP INDEX public.idx_153689_cms_pagemoderatorstate_user_id;
DROP INDEX public.idx_153689_cms_pagemoderatorstate_page_id;
DROP INDEX public.idx_153683_cms_pagemoderator_user_id;
DROP INDEX public.idx_153683_cms_pagemoderator_page_id;
DROP INDEX public.idx_153677_publisher_public_id;
DROP INDEX public.idx_153677_cms_page_tree_id;
DROP INDEX public.idx_153677_cms_page_soft_root;
DROP INDEX public.idx_153677_cms_page_site_id;
DROP INDEX public.idx_153677_cms_page_rght;
DROP INDEX public.idx_153677_cms_page_reverse_id;
DROP INDEX public.idx_153677_cms_page_publisher_state;
DROP INDEX public.idx_153677_cms_page_publisher_is_draft;
DROP INDEX public.idx_153677_cms_page_publication_end_date;
DROP INDEX public.idx_153677_cms_page_publication_date;
DROP INDEX public.idx_153677_cms_page_parent_id;
DROP INDEX public.idx_153677_cms_page_navigation_extenders;
DROP INDEX public.idx_153677_cms_page_lft;
DROP INDEX public.idx_153677_cms_page_level;
DROP INDEX public.idx_153677_cms_page_in_navigation;
DROP INDEX public.idx_153671_site_id_refs_id_38dfe611;
DROP INDEX public.idx_153671_globalpagepermission_id;
DROP INDEX public.idx_153665_cms_globalpagepermission_user_id;
DROP INDEX public.idx_153665_cms_globalpagepermission_group_id;
DROP INDEX public.idx_153659_cms_cmsplugin_tree_id;
DROP INDEX public.idx_153659_cms_cmsplugin_rght;
DROP INDEX public.idx_153659_cms_cmsplugin_plugin_type;
DROP INDEX public.idx_153659_cms_cmsplugin_parent_id;
DROP INDEX public.idx_153659_cms_cmsplugin_lft;
DROP INDEX public.idx_153659_cms_cmsplugin_level;
DROP INDEX public.idx_153659_cms_cmsplugin_language;
DROP INDEX public.idx_153648_cmsplugin_snippetptr_snippet_id;
DROP INDEX public.idx_153642_cmsplugin_picture_page_link_id;
DROP INDEX public.idx_153636_cmsplugin_link_page_link_id;
DROP INDEX public.idx_153623_user_id;
DROP INDEX public.idx_153623_permission_id_refs_id_67e79cb;
DROP INDEX public.idx_153617_user_id;
DROP INDEX public.idx_153617_group_id_refs_id_f116770;
DROP INDEX public.idx_153611_username;
DROP INDEX public.idx_153605_content_type_id;
DROP INDEX public.idx_153605_auth_permission_content_type_id;
DROP INDEX public.idx_153596_auth_message_user_id;
DROP INDEX public.idx_153590_permission_id_refs_id_5886d21f;
DROP INDEX public.idx_153590_group_id;
DROP INDEX public.idx_153584_name;
DROP INDEX public.cms_placeholder_slot_like;
DROP INDEX public.cms_placeholder_slot;
DROP INDEX public.cms_page_placeholders_placeholder_id;
DROP INDEX public.cms_page_placeholders_page_id;
DROP INDEX public.cms_page_limit_visibility_in_menu;
DROP INDEX public.cms_cmsplugin_new_placeholder_id;
ALTER TABLE ONLY public.south_migrationhistory DROP CONSTRAINT south_migrationhistory_pkey;
ALTER TABLE ONLY public.menus_cachekey DROP CONSTRAINT menus_cachekey_pkey;
ALTER TABLE ONLY public.ugc_web_user_user_directory DROP CONSTRAINT idx_154085_primary;
ALTER TABLE ONLY public.ugc_web_user DROP CONSTRAINT idx_154076_primary;
ALTER TABLE ONLY public.ugc_user_directory DROP CONSTRAINT idx_154070_primary;
ALTER TABLE ONLY public.snippet_snippet DROP CONSTRAINT idx_154061_primary;
ALTER TABLE ONLY public.httpproxy_response DROP CONSTRAINT idx_154052_primary;
ALTER TABLE ONLY public.httpproxy_request DROP CONSTRAINT idx_154043_primary;
ALTER TABLE ONLY public.gsettings_global_var_type DROP CONSTRAINT idx_154037_primary;
ALTER TABLE ONLY public.gsettings_global_var_category DROP CONSTRAINT idx_154028_primary;
ALTER TABLE ONLY public.gsettings_global_var DROP CONSTRAINT idx_154019_primary;
ALTER TABLE ONLY public.editions_work DROP CONSTRAINT idx_154013_primary;
ALTER TABLE ONLY public.editions_witness_translation DROP CONSTRAINT idx_154004_primary;
ALTER TABLE ONLY public.editions_witness_transcription DROP CONSTRAINT idx_153995_primary;
ALTER TABLE ONLY public.editions_witness_language DROP CONSTRAINT idx_153989_primary;
ALTER TABLE ONLY public.editions_witness DROP CONSTRAINT idx_153980_primary;
ALTER TABLE ONLY public.editions_version_witness DROP CONSTRAINT idx_153974_primary;
ALTER TABLE ONLY public.editions_version_relationship_type DROP CONSTRAINT idx_153965_primary;
ALTER TABLE ONLY public.editions_version_relationship DROP CONSTRAINT idx_153956_primary;
ALTER TABLE ONLY public.editions_version_language DROP CONSTRAINT idx_153950_primary;
ALTER TABLE ONLY public.editions_version DROP CONSTRAINT idx_153941_primary;
ALTER TABLE ONLY public.editions_user_comment DROP CONSTRAINT idx_153932_primary;
ALTER TABLE ONLY public.editions_topic DROP CONSTRAINT idx_153926_primary;
ALTER TABLE ONLY public.editions_text_attribute_work DROP CONSTRAINT idx_153920_primary;
ALTER TABLE ONLY public.editions_text_attribute DROP CONSTRAINT idx_153914_primary;
ALTER TABLE ONLY public.editions_sigla_provenance DROP CONSTRAINT idx_153908_primary;
ALTER TABLE ONLY public.editions_resource DROP CONSTRAINT idx_153902_primary;
ALTER TABLE ONLY public.editions_place DROP CONSTRAINT idx_153896_primary;
ALTER TABLE ONLY public.editions_person DROP CONSTRAINT idx_153890_primary;
ALTER TABLE ONLY public.editions_manuscript DROP CONSTRAINT idx_153881_primary;
ALTER TABLE ONLY public.editions_language DROP CONSTRAINT idx_153875_primary;
ALTER TABLE ONLY public.editions_king DROP CONSTRAINT idx_153870_primary;
ALTER TABLE ONLY public.editions_hyparchetype DROP CONSTRAINT idx_153863_primary;
ALTER TABLE ONLY public.editions_glossary_term DROP CONSTRAINT idx_153854_primary;
ALTER TABLE ONLY public.editions_folio_side DROP CONSTRAINT idx_153848_primary;
ALTER TABLE ONLY public.editions_folio_image DROP CONSTRAINT idx_153839_primary;
ALTER TABLE ONLY public.editions_eel_edition_status DROP CONSTRAINT idx_153833_primary;
ALTER TABLE ONLY public.editions_editor_edition DROP CONSTRAINT idx_153827_primary;
ALTER TABLE ONLY public.editions_editor DROP CONSTRAINT idx_153821_primary;
ALTER TABLE ONLY public.editions_edition_translation DROP CONSTRAINT idx_153812_primary;
ALTER TABLE ONLY public.editions_edition_bibliographic_entry DROP CONSTRAINT idx_153806_primary;
ALTER TABLE ONLY public.editions_edition DROP CONSTRAINT idx_153797_primary;
ALTER TABLE ONLY public.editions_commentary DROP CONSTRAINT idx_153788_primary;
ALTER TABLE ONLY public.editions_bib_category DROP CONSTRAINT idx_153782_primary;
ALTER TABLE ONLY public.editions_bibliographic_entry_bib_category DROP CONSTRAINT idx_153776_primary;
ALTER TABLE ONLY public.editions_bibliographic_entry DROP CONSTRAINT idx_153767_primary;
ALTER TABLE ONLY public.editions_archive DROP CONSTRAINT idx_153761_primary;
ALTER TABLE ONLY public.django_template_sites DROP CONSTRAINT idx_153755_primary;
ALTER TABLE ONLY public.django_template DROP CONSTRAINT idx_153746_primary;
ALTER TABLE ONLY public.django_site DROP CONSTRAINT idx_153740_primary;
ALTER TABLE ONLY public.django_session DROP CONSTRAINT idx_153732_primary;
ALTER TABLE ONLY public.django_content_type DROP CONSTRAINT idx_153728_primary;
ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT idx_153719_primary;
ALTER TABLE ONLY public.cms_title DROP CONSTRAINT idx_153710_primary;
ALTER TABLE ONLY public.cms_pageusergroup DROP CONSTRAINT idx_153705_primary;
ALTER TABLE ONLY public.cms_pageuser DROP CONSTRAINT idx_153702_primary;
ALTER TABLE ONLY public.cms_pagepermission DROP CONSTRAINT idx_153698_primary;
ALTER TABLE ONLY public.cms_pagemoderatorstate DROP CONSTRAINT idx_153689_primary;
ALTER TABLE ONLY public.cms_pagemoderator DROP CONSTRAINT idx_153683_primary;
ALTER TABLE ONLY public.cms_page DROP CONSTRAINT idx_153677_primary;
ALTER TABLE ONLY public.cms_globalpagepermission_sites DROP CONSTRAINT idx_153671_primary;
ALTER TABLE ONLY public.cms_globalpagepermission DROP CONSTRAINT idx_153665_primary;
ALTER TABLE ONLY public.cms_cmsplugin DROP CONSTRAINT idx_153659_primary;
ALTER TABLE ONLY public.cmsplugin_text DROP CONSTRAINT idx_153651_primary;
ALTER TABLE ONLY public.cmsplugin_snippetptr DROP CONSTRAINT idx_153648_primary;
ALTER TABLE ONLY public.cmsplugin_picture DROP CONSTRAINT idx_153642_primary;
ALTER TABLE ONLY public.cmsplugin_link DROP CONSTRAINT idx_153636_primary;
ALTER TABLE ONLY public.cmsplugin_googlemap DROP CONSTRAINT idx_153630_primary;
ALTER TABLE ONLY public.cmsplugin_file DROP CONSTRAINT idx_153627_primary;
ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT idx_153623_primary;
ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT idx_153617_primary;
ALTER TABLE ONLY public.auth_user DROP CONSTRAINT idx_153611_primary;
ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT idx_153605_primary;
ALTER TABLE ONLY public.auth_message DROP CONSTRAINT idx_153596_primary;
ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT idx_153590_primary;
ALTER TABLE ONLY public.auth_group DROP CONSTRAINT idx_153584_primary;
ALTER TABLE ONLY public.cms_title DROP CONSTRAINT cms_title_page_id_45628dc0e8a26dd5_uniq;
ALTER TABLE ONLY public.cms_placeholder DROP CONSTRAINT cms_placeholder_pkey;
ALTER TABLE ONLY public.cms_page_placeholders DROP CONSTRAINT cms_page_placeholders_pkey;
ALTER TABLE ONLY public.cms_page_placeholders DROP CONSTRAINT cms_page_placeholders_page_id_598353cf6a0df834_uniq;
ALTER TABLE public.ugc_web_user_user_directory ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.ugc_web_user ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.ugc_user_directory ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.south_migrationhistory ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.snippet_snippet ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.menus_cachekey ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.httpproxy_response ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.httpproxy_request ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.gsettings_global_var_type ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.gsettings_global_var_category ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.gsettings_global_var ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.editions_work ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.editions_witness_translation ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.editions_witness_transcription ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.editions_witness_language ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.editions_witness ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.editions_version_witness ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.editions_version_relationship_type ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.editions_version_relationship ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.editions_version_language ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.editions_version ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.editions_user_comment ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.editions_topic ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.editions_text_attribute_work ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.editions_text_attribute ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.editions_sigla_provenance ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.editions_resource ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.editions_place ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.editions_person ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.editions_manuscript ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.editions_language ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.editions_hyparchetype ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.editions_glossary_term ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.editions_folio_side ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.editions_folio_image ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.editions_eel_edition_status ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.editions_editor_edition ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.editions_editor ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.editions_edition_translation ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.editions_edition_bibliographic_entry ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.editions_edition ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.editions_commentary ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.editions_bibliographic_entry_bib_category ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.editions_bibliographic_entry ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.editions_bib_category ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.editions_archive ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.django_template_sites ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.django_template ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.django_site ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.django_content_type ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.django_admin_log ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.cms_title ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.cms_placeholder ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.cms_pagepermission ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.cms_pagemoderatorstate ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.cms_pagemoderator ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.cms_page_placeholders ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.cms_page ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.cms_globalpagepermission_sites ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.cms_globalpagepermission ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.cms_cmsplugin ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.auth_user_user_permissions ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.auth_user_groups ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.auth_user ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.auth_permission ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.auth_message ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.auth_group_permissions ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.auth_group ALTER COLUMN id DROP DEFAULT;
DROP SEQUENCE public.ugc_web_user_user_directory_id_seq;
DROP TABLE public.ugc_web_user_user_directory;
DROP SEQUENCE public.ugc_web_user_id_seq;
DROP TABLE public.ugc_web_user;
DROP SEQUENCE public.ugc_user_directory_id_seq;
DROP TABLE public.ugc_user_directory;
DROP SEQUENCE public.south_migrationhistory_id_seq;
DROP TABLE public.south_migrationhistory;
DROP SEQUENCE public.snippet_snippet_id_seq;
DROP TABLE public.snippet_snippet;
DROP SEQUENCE public.menus_cachekey_id_seq;
DROP TABLE public.menus_cachekey;
DROP SEQUENCE public.httpproxy_response_id_seq;
DROP TABLE public.httpproxy_response;
DROP SEQUENCE public.httpproxy_request_id_seq;
DROP TABLE public.httpproxy_request;
DROP SEQUENCE public.gsettings_global_var_type_id_seq;
DROP TABLE public.gsettings_global_var_type;
DROP SEQUENCE public.gsettings_global_var_id_seq;
DROP SEQUENCE public.gsettings_global_var_category_id_seq;
DROP TABLE public.gsettings_global_var_category;
DROP TABLE public.gsettings_global_var;
DROP SEQUENCE public.editions_work_id_seq;
DROP TABLE public.editions_work;
DROP SEQUENCE public.editions_witness_translation_id_seq;
DROP TABLE public.editions_witness_translation;
DROP SEQUENCE public.editions_witness_transcription_id_seq;
DROP TABLE public.editions_witness_transcription;
DROP SEQUENCE public.editions_witness_language_id_seq;
DROP TABLE public.editions_witness_language;
DROP SEQUENCE public.editions_witness_id_seq;
DROP TABLE public.editions_witness;
DROP SEQUENCE public.editions_version_witness_id_seq;
DROP TABLE public.editions_version_witness;
DROP SEQUENCE public.editions_version_relationship_type_id_seq;
DROP TABLE public.editions_version_relationship_type;
DROP SEQUENCE public.editions_version_relationship_id_seq;
DROP TABLE public.editions_version_relationship;
DROP SEQUENCE public.editions_version_language_id_seq;
DROP TABLE public.editions_version_language;
DROP SEQUENCE public.editions_version_id_seq;
DROP TABLE public.editions_version;
DROP SEQUENCE public.editions_user_comment_id_seq;
DROP TABLE public.editions_user_comment;
DROP SEQUENCE public.editions_topic_id_seq;
DROP TABLE public.editions_topic;
DROP SEQUENCE public.editions_text_attribute_work_id_seq;
DROP TABLE public.editions_text_attribute_work;
DROP SEQUENCE public.editions_text_attribute_id_seq;
DROP TABLE public.editions_text_attribute;
DROP SEQUENCE public.editions_sigla_provenance_id_seq;
DROP TABLE public.editions_sigla_provenance;
DROP SEQUENCE public.editions_resource_id_seq;
DROP TABLE public.editions_resource;
DROP SEQUENCE public.editions_place_id_seq;
DROP TABLE public.editions_place;
DROP SEQUENCE public.editions_person_id_seq;
DROP TABLE public.editions_person;
DROP SEQUENCE public.editions_manuscript_id_seq;
DROP TABLE public.editions_manuscript;
DROP SEQUENCE public.editions_language_id_seq;
DROP TABLE public.editions_language;
DROP TABLE public.editions_king;
DROP SEQUENCE public.editions_hyparchetype_id_seq;
DROP TABLE public.editions_hyparchetype;
DROP SEQUENCE public.editions_glossary_term_id_seq;
DROP TABLE public.editions_glossary_term;
DROP SEQUENCE public.editions_folio_side_id_seq;
DROP TABLE public.editions_folio_side;
DROP SEQUENCE public.editions_folio_image_id_seq;
DROP TABLE public.editions_folio_image;
DROP SEQUENCE public.editions_eel_edition_status_id_seq;
DROP TABLE public.editions_eel_edition_status;
DROP SEQUENCE public.editions_editor_id_seq;
DROP SEQUENCE public.editions_editor_edition_id_seq;
DROP TABLE public.editions_editor_edition;
DROP TABLE public.editions_editor;
DROP SEQUENCE public.editions_edition_translation_id_seq;
DROP TABLE public.editions_edition_translation;
DROP SEQUENCE public.editions_edition_id_seq;
DROP SEQUENCE public.editions_edition_bibliographic_entry_id_seq;
DROP TABLE public.editions_edition_bibliographic_entry;
DROP TABLE public.editions_edition;
DROP SEQUENCE public.editions_commentary_id_seq;
DROP TABLE public.editions_commentary;
DROP SEQUENCE public.editions_bibliographic_entry_id_seq;
DROP SEQUENCE public.editions_bibliographic_entry_bib_category_id_seq;
DROP TABLE public.editions_bibliographic_entry_bib_category;
DROP TABLE public.editions_bibliographic_entry;
DROP SEQUENCE public.editions_bib_category_id_seq;
DROP TABLE public.editions_bib_category;
DROP SEQUENCE public.editions_archive_id_seq;
DROP TABLE public.editions_archive;
DROP SEQUENCE public.django_template_sites_id_seq;
DROP TABLE public.django_template_sites;
DROP SEQUENCE public.django_template_id_seq;
DROP TABLE public.django_template;
DROP SEQUENCE public.django_site_id_seq;
DROP TABLE public.django_site;
DROP TABLE public.django_session;
DROP SEQUENCE public.django_content_type_id_seq;
DROP TABLE public.django_content_type;
DROP SEQUENCE public.django_admin_log_id_seq;
DROP TABLE public.django_admin_log;
DROP TABLE public.cmsplugin_text;
DROP TABLE public.cmsplugin_snippetptr;
DROP TABLE public.cmsplugin_picture;
DROP TABLE public.cmsplugin_link;
DROP TABLE public.cmsplugin_googlemap;
DROP TABLE public.cmsplugin_file;
DROP SEQUENCE public.cms_title_id_seq;
DROP TABLE public.cms_title;
DROP SEQUENCE public.cms_placeholder_id_seq;
DROP TABLE public.cms_placeholder;
DROP TABLE public.cms_pageusergroup;
DROP TABLE public.cms_pageuser;
DROP SEQUENCE public.cms_pagepermission_id_seq;
DROP TABLE public.cms_pagepermission;
DROP SEQUENCE public.cms_pagemoderatorstate_id_seq;
DROP TABLE public.cms_pagemoderatorstate;
DROP SEQUENCE public.cms_pagemoderator_id_seq;
DROP TABLE public.cms_pagemoderator;
DROP SEQUENCE public.cms_page_placeholders_id_seq;
DROP TABLE public.cms_page_placeholders;
DROP SEQUENCE public.cms_page_id_seq;
DROP TABLE public.cms_page;
DROP SEQUENCE public.cms_globalpagepermission_sites_id_seq;
DROP TABLE public.cms_globalpagepermission_sites;
DROP SEQUENCE public.cms_globalpagepermission_id_seq;
DROP TABLE public.cms_globalpagepermission;
DROP SEQUENCE public.cms_cmsplugin_id_seq;
DROP TABLE public.cms_cmsplugin;
DROP SEQUENCE public.auth_user_user_permissions_id_seq;
DROP TABLE public.auth_user_user_permissions;
DROP SEQUENCE public.auth_user_id_seq;
DROP SEQUENCE public.auth_user_groups_id_seq;
DROP TABLE public.auth_user_groups;
DROP TABLE public.auth_user;
DROP SEQUENCE public.auth_permission_id_seq;
DROP TABLE public.auth_permission;
DROP SEQUENCE public.auth_message_id_seq;
DROP TABLE public.auth_message;
DROP SEQUENCE public.auth_group_permissions_id_seq;
DROP TABLE public.auth_group_permissions;
DROP SEQUENCE public.auth_group_id_seq;
DROP TABLE public.auth_group;
DROP EXTENSION plpgsql;
DROP SCHEMA public;
--
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO postgres;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS 'standard public schema';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.auth_group (
    id bigint NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO app_eel;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO app_eel;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id bigint NOT NULL,
    permission_id bigint NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO app_eel;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO app_eel;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_message; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.auth_message (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    message text NOT NULL
);


ALTER TABLE public.auth_message OWNER TO app_eel;

--
-- Name: auth_message_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.auth_message_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_message_id_seq OWNER TO app_eel;

--
-- Name: auth_message_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.auth_message_id_seq OWNED BY public.auth_message.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.auth_permission (
    id bigint NOT NULL,
    name character varying(150) NOT NULL,
    content_type_id bigint NOT NULL,
    codename character varying(200) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO app_eel;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO app_eel;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.auth_user (
    id bigint NOT NULL,
    username character varying(30) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(75) NOT NULL,
    password character varying(128) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    is_superuser boolean NOT NULL,
    last_login timestamp with time zone NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO app_eel;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.auth_user_groups (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    group_id bigint NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO app_eel;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO app_eel;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.auth_user_groups_id_seq OWNED BY public.auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO app_eel;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.auth_user_id_seq OWNED BY public.auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.auth_user_user_permissions (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    permission_id bigint NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO app_eel;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO app_eel;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.auth_user_user_permissions_id_seq OWNED BY public.auth_user_user_permissions.id;


--
-- Name: cms_cmsplugin; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.cms_cmsplugin (
    id bigint NOT NULL,
    parent_id bigint,
    "position" smallint,
    language character varying(15) NOT NULL,
    plugin_type character varying(50) NOT NULL,
    creation_date timestamp with time zone NOT NULL,
    level bigint NOT NULL,
    lft bigint NOT NULL,
    rght bigint NOT NULL,
    tree_id bigint NOT NULL,
    placeholder_id integer
);


ALTER TABLE public.cms_cmsplugin OWNER TO app_eel;

--
-- Name: cms_cmsplugin_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.cms_cmsplugin_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cms_cmsplugin_id_seq OWNER TO app_eel;

--
-- Name: cms_cmsplugin_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.cms_cmsplugin_id_seq OWNED BY public.cms_cmsplugin.id;


--
-- Name: cms_globalpagepermission; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.cms_globalpagepermission (
    id bigint NOT NULL,
    user_id bigint,
    group_id bigint,
    can_change boolean NOT NULL,
    can_add boolean NOT NULL,
    can_delete boolean NOT NULL,
    can_change_advanced_settings boolean NOT NULL,
    can_publish boolean NOT NULL,
    can_change_permissions boolean NOT NULL,
    can_move_page boolean NOT NULL,
    can_moderate boolean NOT NULL,
    can_recover_page boolean NOT NULL
);


ALTER TABLE public.cms_globalpagepermission OWNER TO app_eel;

--
-- Name: cms_globalpagepermission_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.cms_globalpagepermission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cms_globalpagepermission_id_seq OWNER TO app_eel;

--
-- Name: cms_globalpagepermission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.cms_globalpagepermission_id_seq OWNED BY public.cms_globalpagepermission.id;


--
-- Name: cms_globalpagepermission_sites; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.cms_globalpagepermission_sites (
    id bigint NOT NULL,
    globalpagepermission_id bigint NOT NULL,
    site_id bigint NOT NULL
);


ALTER TABLE public.cms_globalpagepermission_sites OWNER TO app_eel;

--
-- Name: cms_globalpagepermission_sites_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.cms_globalpagepermission_sites_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cms_globalpagepermission_sites_id_seq OWNER TO app_eel;

--
-- Name: cms_globalpagepermission_sites_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.cms_globalpagepermission_sites_id_seq OWNED BY public.cms_globalpagepermission_sites.id;


--
-- Name: cms_page; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.cms_page (
    id bigint NOT NULL,
    publisher_is_draft boolean NOT NULL,
    publisher_public_id bigint,
    publisher_state smallint NOT NULL,
    created_by character varying(70) NOT NULL,
    changed_by character varying(70) NOT NULL,
    parent_id bigint,
    creation_date timestamp with time zone NOT NULL,
    publication_date timestamp with time zone,
    publication_end_date timestamp with time zone,
    in_navigation boolean NOT NULL,
    soft_root boolean NOT NULL,
    reverse_id character varying(40),
    navigation_extenders character varying(80),
    published boolean NOT NULL,
    template character varying(100) NOT NULL,
    site_id bigint NOT NULL,
    moderator_state smallint NOT NULL,
    level bigint NOT NULL,
    lft bigint NOT NULL,
    rght bigint NOT NULL,
    tree_id bigint NOT NULL,
    login_required boolean NOT NULL,
    limit_visibility_in_menu smallint
);


ALTER TABLE public.cms_page OWNER TO app_eel;

--
-- Name: cms_page_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.cms_page_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cms_page_id_seq OWNER TO app_eel;

--
-- Name: cms_page_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.cms_page_id_seq OWNED BY public.cms_page.id;


--
-- Name: cms_page_placeholders; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.cms_page_placeholders (
    id integer NOT NULL,
    page_id integer NOT NULL,
    placeholder_id integer NOT NULL
);


ALTER TABLE public.cms_page_placeholders OWNER TO app_eel;

--
-- Name: cms_page_placeholders_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.cms_page_placeholders_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cms_page_placeholders_id_seq OWNER TO app_eel;

--
-- Name: cms_page_placeholders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.cms_page_placeholders_id_seq OWNED BY public.cms_page_placeholders.id;


--
-- Name: cms_pagemoderator; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.cms_pagemoderator (
    id bigint NOT NULL,
    page_id bigint NOT NULL,
    user_id bigint NOT NULL,
    moderate_page boolean NOT NULL,
    moderate_children boolean NOT NULL,
    moderate_descendants boolean NOT NULL
);


ALTER TABLE public.cms_pagemoderator OWNER TO app_eel;

--
-- Name: cms_pagemoderator_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.cms_pagemoderator_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cms_pagemoderator_id_seq OWNER TO app_eel;

--
-- Name: cms_pagemoderator_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.cms_pagemoderator_id_seq OWNED BY public.cms_pagemoderator.id;


--
-- Name: cms_pagemoderatorstate; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.cms_pagemoderatorstate (
    id bigint NOT NULL,
    page_id bigint NOT NULL,
    user_id bigint,
    created timestamp with time zone NOT NULL,
    action character varying(3),
    message text NOT NULL
);


ALTER TABLE public.cms_pagemoderatorstate OWNER TO app_eel;

--
-- Name: cms_pagemoderatorstate_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.cms_pagemoderatorstate_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cms_pagemoderatorstate_id_seq OWNER TO app_eel;

--
-- Name: cms_pagemoderatorstate_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.cms_pagemoderatorstate_id_seq OWNED BY public.cms_pagemoderatorstate.id;


--
-- Name: cms_pagepermission; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.cms_pagepermission (
    id bigint NOT NULL,
    user_id bigint,
    group_id bigint,
    can_change boolean NOT NULL,
    can_add boolean NOT NULL,
    can_delete boolean NOT NULL,
    can_change_advanced_settings boolean NOT NULL,
    can_publish boolean NOT NULL,
    can_change_permissions boolean NOT NULL,
    can_move_page boolean NOT NULL,
    can_moderate boolean NOT NULL,
    grant_on bigint NOT NULL,
    page_id bigint
);


ALTER TABLE public.cms_pagepermission OWNER TO app_eel;

--
-- Name: cms_pagepermission_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.cms_pagepermission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cms_pagepermission_id_seq OWNER TO app_eel;

--
-- Name: cms_pagepermission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.cms_pagepermission_id_seq OWNED BY public.cms_pagepermission.id;


--
-- Name: cms_pageuser; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.cms_pageuser (
    user_ptr_id bigint NOT NULL,
    created_by_id bigint NOT NULL
);


ALTER TABLE public.cms_pageuser OWNER TO app_eel;

--
-- Name: cms_pageusergroup; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.cms_pageusergroup (
    group_ptr_id bigint NOT NULL,
    created_by_id bigint NOT NULL
);


ALTER TABLE public.cms_pageusergroup OWNER TO app_eel;

--
-- Name: cms_placeholder; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.cms_placeholder (
    slot character varying(50) NOT NULL,
    id integer NOT NULL,
    default_width smallint,
    CONSTRAINT ck_default_width_pstv_520fa3f1292fc5fe CHECK ((default_width >= 0)),
    CONSTRAINT cms_placeholder_default_width_check CHECK ((default_width >= 0))
);


ALTER TABLE public.cms_placeholder OWNER TO app_eel;

--
-- Name: cms_placeholder_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.cms_placeholder_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cms_placeholder_id_seq OWNER TO app_eel;

--
-- Name: cms_placeholder_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.cms_placeholder_id_seq OWNED BY public.cms_placeholder.id;


--
-- Name: cms_title; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.cms_title (
    id bigint NOT NULL,
    language character varying(15) NOT NULL,
    title character varying(255) NOT NULL,
    menu_title character varying(255),
    slug character varying(255) NOT NULL,
    path character varying(255) NOT NULL,
    has_url_overwrite boolean NOT NULL,
    application_urls character varying(200),
    redirect character varying(255),
    meta_description text,
    meta_keywords character varying(255),
    page_title character varying(255),
    page_id bigint NOT NULL,
    creation_date timestamp with time zone NOT NULL
);


ALTER TABLE public.cms_title OWNER TO app_eel;

--
-- Name: cms_title_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.cms_title_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cms_title_id_seq OWNER TO app_eel;

--
-- Name: cms_title_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.cms_title_id_seq OWNED BY public.cms_title.id;


--
-- Name: cmsplugin_file; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.cmsplugin_file (
    cmsplugin_ptr_id bigint NOT NULL,
    file character varying(100) NOT NULL,
    title character varying(255)
);


ALTER TABLE public.cmsplugin_file OWNER TO app_eel;

--
-- Name: cmsplugin_googlemap; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.cmsplugin_googlemap (
    cmsplugin_ptr_id bigint NOT NULL,
    title character varying(100),
    address character varying(150) NOT NULL,
    zipcode character varying(30) NOT NULL,
    city character varying(100) NOT NULL,
    content character varying(255),
    zoom bigint,
    lat numeric(10,6),
    lng numeric(10,6),
    route_planer_title character varying(150),
    route_planer boolean NOT NULL
);


ALTER TABLE public.cmsplugin_googlemap OWNER TO app_eel;

--
-- Name: cmsplugin_link; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.cmsplugin_link (
    cmsplugin_ptr_id bigint NOT NULL,
    name character varying(256) NOT NULL,
    url character varying(200),
    page_link_id bigint,
    mailto character varying(75)
);


ALTER TABLE public.cmsplugin_link OWNER TO app_eel;

--
-- Name: cmsplugin_picture; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.cmsplugin_picture (
    cmsplugin_ptr_id bigint NOT NULL,
    image character varying(100) NOT NULL,
    url character varying(255),
    page_link_id bigint,
    alt character varying(255),
    longdesc character varying(255),
    "float" character varying(10)
);


ALTER TABLE public.cmsplugin_picture OWNER TO app_eel;

--
-- Name: cmsplugin_snippetptr; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.cmsplugin_snippetptr (
    cmsplugin_ptr_id bigint NOT NULL,
    snippet_id bigint NOT NULL
);


ALTER TABLE public.cmsplugin_snippetptr OWNER TO app_eel;

--
-- Name: cmsplugin_text; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.cmsplugin_text (
    cmsplugin_ptr_id bigint NOT NULL,
    body text NOT NULL
);


ALTER TABLE public.cmsplugin_text OWNER TO app_eel;

--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.django_admin_log (
    id bigint NOT NULL,
    action_time timestamp with time zone NOT NULL,
    user_id bigint NOT NULL,
    content_type_id bigint,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL
);


ALTER TABLE public.django_admin_log OWNER TO app_eel;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO app_eel;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.django_content_type (
    id bigint NOT NULL,
    name character varying(100) NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO app_eel;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO app_eel;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO app_eel;

--
-- Name: django_site; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.django_site (
    id bigint NOT NULL,
    domain character varying(100) NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.django_site OWNER TO app_eel;

--
-- Name: django_site_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.django_site_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_site_id_seq OWNER TO app_eel;

--
-- Name: django_site_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.django_site_id_seq OWNED BY public.django_site.id;


--
-- Name: django_template; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.django_template (
    id bigint NOT NULL,
    name character varying(100) NOT NULL,
    content text NOT NULL,
    creation_date timestamp with time zone NOT NULL,
    last_changed timestamp with time zone NOT NULL
);


ALTER TABLE public.django_template OWNER TO app_eel;

--
-- Name: django_template_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.django_template_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_template_id_seq OWNER TO app_eel;

--
-- Name: django_template_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.django_template_id_seq OWNED BY public.django_template.id;


--
-- Name: django_template_sites; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.django_template_sites (
    id bigint NOT NULL,
    template_id bigint NOT NULL,
    site_id bigint NOT NULL
);


ALTER TABLE public.django_template_sites OWNER TO app_eel;

--
-- Name: django_template_sites_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.django_template_sites_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_template_sites_id_seq OWNER TO app_eel;

--
-- Name: django_template_sites_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.django_template_sites_id_seq OWNED BY public.django_template_sites.id;


--
-- Name: editions_archive; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.editions_archive (
    country character varying(128) NOT NULL,
    id bigint NOT NULL,
    name character varying(128) NOT NULL,
    city character varying(128) NOT NULL
);


ALTER TABLE public.editions_archive OWNER TO app_eel;

--
-- Name: editions_archive_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.editions_archive_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.editions_archive_id_seq OWNER TO app_eel;

--
-- Name: editions_archive_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.editions_archive_id_seq OWNED BY public.editions_archive.id;


--
-- Name: editions_bib_category; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.editions_bib_category (
    id bigint NOT NULL,
    name character varying(128) NOT NULL
);


ALTER TABLE public.editions_bib_category OWNER TO app_eel;

--
-- Name: editions_bib_category_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.editions_bib_category_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.editions_bib_category_id_seq OWNER TO app_eel;

--
-- Name: editions_bib_category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.editions_bib_category_id_seq OWNED BY public.editions_bib_category.id;


--
-- Name: editions_bibliographic_entry; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.editions_bibliographic_entry (
    id bigint NOT NULL,
    styled_reference text NOT NULL,
    authors character varying(255) NOT NULL,
    title_article character varying(1024) NOT NULL,
    title_monograph character varying(1024) NOT NULL,
    publication_date bigint,
    language_id bigint NOT NULL,
    created date
);


ALTER TABLE public.editions_bibliographic_entry OWNER TO app_eel;

--
-- Name: editions_bibliographic_entry_bib_category; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.editions_bibliographic_entry_bib_category (
    id bigint NOT NULL,
    bibliographic_entry_id bigint NOT NULL,
    bib_category_id bigint NOT NULL
);


ALTER TABLE public.editions_bibliographic_entry_bib_category OWNER TO app_eel;

--
-- Name: editions_bibliographic_entry_bib_category_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.editions_bibliographic_entry_bib_category_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.editions_bibliographic_entry_bib_category_id_seq OWNER TO app_eel;

--
-- Name: editions_bibliographic_entry_bib_category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.editions_bibliographic_entry_bib_category_id_seq OWNED BY public.editions_bibliographic_entry_bib_category.id;


--
-- Name: editions_bibliographic_entry_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.editions_bibliographic_entry_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.editions_bibliographic_entry_id_seq OWNER TO app_eel;

--
-- Name: editions_bibliographic_entry_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.editions_bibliographic_entry_id_seq OWNED BY public.editions_bibliographic_entry.id;


--
-- Name: editions_commentary; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.editions_commentary (
    id bigint NOT NULL,
    text text NOT NULL,
    updated timestamp with time zone,
    user_id bigint NOT NULL,
    edition_id bigint NOT NULL,
    elementid character varying(32) NOT NULL,
    sort_order bigint
);


ALTER TABLE public.editions_commentary OWNER TO app_eel;

--
-- Name: editions_commentary_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.editions_commentary_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.editions_commentary_id_seq OWNER TO app_eel;

--
-- Name: editions_commentary_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.editions_commentary_id_seq OWNED BY public.editions_commentary.id;


--
-- Name: editions_edition; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.editions_edition (
    date_of_edition date,
    text text NOT NULL,
    date_of_edition_mod smallint NOT NULL,
    version_id bigint NOT NULL,
    date_of_edition_to date,
    id bigint NOT NULL,
    eel_edition_status_id bigint NOT NULL,
    abbreviation character varying(32) NOT NULL,
    internal_notes text NOT NULL,
    edition_translation_id bigint,
    introduction text NOT NULL,
    rendered_translation text NOT NULL,
    rendered_apparatus text NOT NULL,
    rendered_edition text NOT NULL,
    rendered_commentary text NOT NULL
);


ALTER TABLE public.editions_edition OWNER TO app_eel;

--
-- Name: editions_edition_bibliographic_entry; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.editions_edition_bibliographic_entry (
    id bigint NOT NULL,
    edition_id bigint NOT NULL,
    bibliographic_entry_id bigint NOT NULL,
    page_ranges character varying(32) NOT NULL
);


ALTER TABLE public.editions_edition_bibliographic_entry OWNER TO app_eel;

--
-- Name: editions_edition_bibliographic_entry_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.editions_edition_bibliographic_entry_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.editions_edition_bibliographic_entry_id_seq OWNER TO app_eel;

--
-- Name: editions_edition_bibliographic_entry_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.editions_edition_bibliographic_entry_id_seq OWNED BY public.editions_edition_bibliographic_entry.id;


--
-- Name: editions_edition_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.editions_edition_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.editions_edition_id_seq OWNER TO app_eel;

--
-- Name: editions_edition_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.editions_edition_id_seq OWNED BY public.editions_edition.id;


--
-- Name: editions_edition_translation; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.editions_edition_translation (
    text text NOT NULL,
    id bigint NOT NULL
);


ALTER TABLE public.editions_edition_translation OWNER TO app_eel;

--
-- Name: editions_edition_translation_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.editions_edition_translation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.editions_edition_translation_id_seq OWNER TO app_eel;

--
-- Name: editions_edition_translation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.editions_edition_translation_id_seq OWNED BY public.editions_edition_translation.id;


--
-- Name: editions_editor; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.editions_editor (
    id bigint NOT NULL,
    abbreviation character varying(32) NOT NULL,
    first_name character varying(32) NOT NULL,
    last_name character varying(32) NOT NULL
);


ALTER TABLE public.editions_editor OWNER TO app_eel;

--
-- Name: editions_editor_edition; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.editions_editor_edition (
    edition_id bigint NOT NULL,
    editor_id bigint NOT NULL,
    id bigint NOT NULL
);


ALTER TABLE public.editions_editor_edition OWNER TO app_eel;

--
-- Name: editions_editor_edition_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.editions_editor_edition_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.editions_editor_edition_id_seq OWNER TO app_eel;

--
-- Name: editions_editor_edition_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.editions_editor_edition_id_seq OWNED BY public.editions_editor_edition.id;


--
-- Name: editions_editor_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.editions_editor_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.editions_editor_id_seq OWNER TO app_eel;

--
-- Name: editions_editor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.editions_editor_id_seq OWNED BY public.editions_editor.id;


--
-- Name: editions_eel_edition_status; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.editions_eel_edition_status (
    id bigint NOT NULL,
    name character varying(32) NOT NULL
);


ALTER TABLE public.editions_eel_edition_status OWNER TO app_eel;

--
-- Name: editions_eel_edition_status_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.editions_eel_edition_status_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.editions_eel_edition_status_id_seq OWNER TO app_eel;

--
-- Name: editions_eel_edition_status_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.editions_eel_edition_status_id_seq OWNED BY public.editions_eel_edition_status.id;


--
-- Name: editions_folio_image; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.editions_folio_image (
    id bigint NOT NULL,
    filename character varying(128) NOT NULL,
    manuscript_id bigint NOT NULL,
    folio_number character varying(8) NOT NULL,
    display_order bigint,
    internal_notes character varying(1024) NOT NULL,
    filepath character varying(128) NOT NULL,
    batch character varying(32) NOT NULL,
    page character varying(8) NOT NULL,
    folio_side_id bigint NOT NULL,
    path character varying(128) NOT NULL,
    filename_sort_order bigint,
    archived boolean NOT NULL
);


ALTER TABLE public.editions_folio_image OWNER TO app_eel;

--
-- Name: editions_folio_image_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.editions_folio_image_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.editions_folio_image_id_seq OWNER TO app_eel;

--
-- Name: editions_folio_image_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.editions_folio_image_id_seq OWNED BY public.editions_folio_image.id;


--
-- Name: editions_folio_side; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.editions_folio_side (
    id bigint NOT NULL,
    name character varying(32) NOT NULL
);


ALTER TABLE public.editions_folio_side OWNER TO app_eel;

--
-- Name: editions_folio_side_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.editions_folio_side_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.editions_folio_side_id_seq OWNER TO app_eel;

--
-- Name: editions_folio_side_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.editions_folio_side_id_seq OWNED BY public.editions_folio_side.id;


--
-- Name: editions_glossary_term; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.editions_glossary_term (
    id bigint NOT NULL,
    term character varying(32) NOT NULL,
    description text NOT NULL
);


ALTER TABLE public.editions_glossary_term OWNER TO app_eel;

--
-- Name: editions_glossary_term_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.editions_glossary_term_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.editions_glossary_term_id_seq OWNER TO app_eel;

--
-- Name: editions_glossary_term_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.editions_glossary_term_id_seq OWNED BY public.editions_glossary_term.id;


--
-- Name: editions_hyparchetype; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.editions_hyparchetype (
    description character varying(1024) NOT NULL,
    edition_id bigint NOT NULL,
    id bigint NOT NULL,
    sigla character varying(32) NOT NULL
);


ALTER TABLE public.editions_hyparchetype OWNER TO app_eel;

--
-- Name: editions_hyparchetype_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.editions_hyparchetype_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.editions_hyparchetype_id_seq OWNER TO app_eel;

--
-- Name: editions_hyparchetype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.editions_hyparchetype_id_seq OWNED BY public.editions_hyparchetype.id;


--
-- Name: editions_king; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.editions_king (
    beginning_regnal_year_to date,
    beginning_regnal_year_mod smallint NOT NULL,
    beginning_regnal_year date,
    end_regnal_year_to date,
    end_regnal_year_mod smallint NOT NULL,
    end_regnal_year date,
    person_ptr_id bigint NOT NULL
);


ALTER TABLE public.editions_king OWNER TO app_eel;

--
-- Name: editions_language; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.editions_language (
    id bigint NOT NULL,
    name character varying(32) NOT NULL,
    color character varying(8) NOT NULL
);


ALTER TABLE public.editions_language OWNER TO app_eel;

--
-- Name: editions_language_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.editions_language_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.editions_language_id_seq OWNER TO app_eel;

--
-- Name: editions_language_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.editions_language_id_seq OWNED BY public.editions_language.id;


--
-- Name: editions_manuscript; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.editions_manuscript (
    id bigint NOT NULL,
    shelf_mark character varying(128) NOT NULL,
    description text NOT NULL,
    archive_id bigint NOT NULL,
    sigla character varying(32) NOT NULL,
    sigla_provenance_id bigint NOT NULL,
    slug character varying(250) NOT NULL,
    hide_from_listings boolean NOT NULL,
    checked_folios boolean NOT NULL,
    single_sheet boolean NOT NULL,
    hide_folio_numbers boolean NOT NULL,
    standard_edition boolean NOT NULL
);


ALTER TABLE public.editions_manuscript OWNER TO app_eel;

--
-- Name: editions_manuscript_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.editions_manuscript_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.editions_manuscript_id_seq OWNER TO app_eel;

--
-- Name: editions_manuscript_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.editions_manuscript_id_seq OWNED BY public.editions_manuscript.id;


--
-- Name: editions_person; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.editions_person (
    id bigint NOT NULL,
    name character varying(32)
);


ALTER TABLE public.editions_person OWNER TO app_eel;

--
-- Name: editions_person_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.editions_person_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.editions_person_id_seq OWNER TO app_eel;

--
-- Name: editions_person_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.editions_person_id_seq OWNED BY public.editions_person.id;


--
-- Name: editions_place; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.editions_place (
    id bigint NOT NULL,
    name character varying(32) NOT NULL
);


ALTER TABLE public.editions_place OWNER TO app_eel;

--
-- Name: editions_place_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.editions_place_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.editions_place_id_seq OWNER TO app_eel;

--
-- Name: editions_place_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.editions_place_id_seq OWNED BY public.editions_place.id;


--
-- Name: editions_resource; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.editions_resource (
    id bigint NOT NULL,
    title character varying(128) NOT NULL,
    caption character varying(255) NOT NULL,
    file character varying(100) NOT NULL
);


ALTER TABLE public.editions_resource OWNER TO app_eel;

--
-- Name: editions_resource_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.editions_resource_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.editions_resource_id_seq OWNER TO app_eel;

--
-- Name: editions_resource_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.editions_resource_id_seq OWNED BY public.editions_resource.id;


--
-- Name: editions_sigla_provenance; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.editions_sigla_provenance (
    id bigint NOT NULL,
    name character varying(32) NOT NULL
);


ALTER TABLE public.editions_sigla_provenance OWNER TO app_eel;

--
-- Name: editions_sigla_provenance_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.editions_sigla_provenance_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.editions_sigla_provenance_id_seq OWNER TO app_eel;

--
-- Name: editions_sigla_provenance_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.editions_sigla_provenance_id_seq OWNED BY public.editions_sigla_provenance.id;


--
-- Name: editions_text_attribute; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.editions_text_attribute (
    id bigint NOT NULL,
    name character varying(32) NOT NULL
);


ALTER TABLE public.editions_text_attribute OWNER TO app_eel;

--
-- Name: editions_text_attribute_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.editions_text_attribute_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.editions_text_attribute_id_seq OWNER TO app_eel;

--
-- Name: editions_text_attribute_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.editions_text_attribute_id_seq OWNED BY public.editions_text_attribute.id;


--
-- Name: editions_text_attribute_work; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.editions_text_attribute_work (
    id bigint NOT NULL,
    text_attribute_id bigint NOT NULL,
    work_id bigint NOT NULL
);


ALTER TABLE public.editions_text_attribute_work OWNER TO app_eel;

--
-- Name: editions_text_attribute_work_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.editions_text_attribute_work_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.editions_text_attribute_work_id_seq OWNER TO app_eel;

--
-- Name: editions_text_attribute_work_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.editions_text_attribute_work_id_seq OWNED BY public.editions_text_attribute_work.id;


--
-- Name: editions_topic; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.editions_topic (
    id bigint NOT NULL,
    name character varying(32) NOT NULL
);


ALTER TABLE public.editions_topic OWNER TO app_eel;

--
-- Name: editions_topic_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.editions_topic_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.editions_topic_id_seq OWNER TO app_eel;

--
-- Name: editions_topic_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.editions_topic_id_seq OWNED BY public.editions_topic.id;


--
-- Name: editions_user_comment; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.editions_user_comment (
    id bigint NOT NULL,
    userid bigint,
    comment text NOT NULL,
    content_type bigint,
    objectid bigint,
    division character varying(32) NOT NULL,
    private boolean NOT NULL,
    archived boolean NOT NULL,
    "timestamp" timestamp with time zone,
    editionid bigint
);


ALTER TABLE public.editions_user_comment OWNER TO app_eel;

--
-- Name: editions_user_comment_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.editions_user_comment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.editions_user_comment_id_seq OWNER TO app_eel;

--
-- Name: editions_user_comment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.editions_user_comment_id_seq OWNED BY public.editions_user_comment.id;


--
-- Name: editions_version; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.editions_version (
    id bigint NOT NULL,
    standard_abbreviation character varying(32) NOT NULL,
    name character varying(128) NOT NULL,
    synopsis text NOT NULL,
    work_id bigint NOT NULL,
    slug character varying(250) NOT NULL,
    synopsis_manuscripts text NOT NULL,
    print_editions text NOT NULL,
    graph text NOT NULL,
    date_to date,
    date_mod smallint NOT NULL,
    date date
);


ALTER TABLE public.editions_version OWNER TO app_eel;

--
-- Name: editions_version_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.editions_version_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.editions_version_id_seq OWNER TO app_eel;

--
-- Name: editions_version_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.editions_version_id_seq OWNED BY public.editions_version.id;


--
-- Name: editions_version_language; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.editions_version_language (
    id bigint NOT NULL,
    version_id bigint NOT NULL,
    language_id bigint NOT NULL
);


ALTER TABLE public.editions_version_language OWNER TO app_eel;

--
-- Name: editions_version_language_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.editions_version_language_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.editions_version_language_id_seq OWNER TO app_eel;

--
-- Name: editions_version_language_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.editions_version_language_id_seq OWNED BY public.editions_version_language.id;


--
-- Name: editions_version_relationship; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.editions_version_relationship (
    id bigint NOT NULL,
    version_relationship_type_id bigint NOT NULL,
    description text NOT NULL,
    source_id bigint NOT NULL,
    target_id bigint NOT NULL
);


ALTER TABLE public.editions_version_relationship OWNER TO app_eel;

--
-- Name: editions_version_relationship_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.editions_version_relationship_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.editions_version_relationship_id_seq OWNER TO app_eel;

--
-- Name: editions_version_relationship_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.editions_version_relationship_id_seq OWNED BY public.editions_version_relationship.id;


--
-- Name: editions_version_relationship_type; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.editions_version_relationship_type (
    id bigint NOT NULL,
    name character varying(128) NOT NULL,
    description text NOT NULL
);


ALTER TABLE public.editions_version_relationship_type OWNER TO app_eel;

--
-- Name: editions_version_relationship_type_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.editions_version_relationship_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.editions_version_relationship_type_id_seq OWNER TO app_eel;

--
-- Name: editions_version_relationship_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.editions_version_relationship_type_id_seq OWNED BY public.editions_version_relationship_type.id;


--
-- Name: editions_version_witness; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.editions_version_witness (
    witness_id bigint NOT NULL,
    id bigint NOT NULL,
    version_id bigint NOT NULL
);


ALTER TABLE public.editions_version_witness OWNER TO app_eel;

--
-- Name: editions_version_witness_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.editions_version_witness_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.editions_version_witness_id_seq OWNER TO app_eel;

--
-- Name: editions_version_witness_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.editions_version_witness_id_seq OWNED BY public.editions_version_witness.id;


--
-- Name: editions_witness; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.editions_witness (
    description text NOT NULL,
    manuscript_id bigint NOT NULL,
    medieval_translation boolean NOT NULL,
    id bigint NOT NULL,
    work_id bigint NOT NULL,
    range_end character varying(8) NOT NULL,
    range_start character varying(8) NOT NULL,
    page boolean NOT NULL,
    witness_transcription_id bigint,
    hide_from_listings boolean NOT NULL,
    rendered_facsimiles text NOT NULL
);


ALTER TABLE public.editions_witness OWNER TO app_eel;

--
-- Name: editions_witness_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.editions_witness_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.editions_witness_id_seq OWNER TO app_eel;

--
-- Name: editions_witness_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.editions_witness_id_seq OWNED BY public.editions_witness.id;


--
-- Name: editions_witness_language; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.editions_witness_language (
    witness_id bigint NOT NULL,
    id bigint NOT NULL,
    language_id bigint NOT NULL
);


ALTER TABLE public.editions_witness_language OWNER TO app_eel;

--
-- Name: editions_witness_language_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.editions_witness_language_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.editions_witness_language_id_seq OWNER TO app_eel;

--
-- Name: editions_witness_language_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.editions_witness_language_id_seq OWNED BY public.editions_witness_language.id;


--
-- Name: editions_witness_transcription; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.editions_witness_transcription (
    text text NOT NULL,
    id bigint NOT NULL,
    witness_translation_id bigint,
    rendered_text text NOT NULL
);


ALTER TABLE public.editions_witness_transcription OWNER TO app_eel;

--
-- Name: editions_witness_transcription_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.editions_witness_transcription_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.editions_witness_transcription_id_seq OWNER TO app_eel;

--
-- Name: editions_witness_transcription_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.editions_witness_transcription_id_seq OWNED BY public.editions_witness_transcription.id;


--
-- Name: editions_witness_translation; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.editions_witness_translation (
    text text NOT NULL,
    id bigint NOT NULL,
    rendered_text text NOT NULL
);


ALTER TABLE public.editions_witness_translation OWNER TO app_eel;

--
-- Name: editions_witness_translation_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.editions_witness_translation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.editions_witness_translation_id_seq OWNER TO app_eel;

--
-- Name: editions_witness_translation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.editions_witness_translation_id_seq OWNED BY public.editions_witness_translation.id;


--
-- Name: editions_work; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.editions_work (
    id bigint NOT NULL,
    name character varying(128) NOT NULL,
    king_id bigint,
    date_mod smallint NOT NULL,
    date_to date,
    date date
);


ALTER TABLE public.editions_work OWNER TO app_eel;

--
-- Name: editions_work_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.editions_work_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.editions_work_id_seq OWNER TO app_eel;

--
-- Name: editions_work_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.editions_work_id_seq OWNED BY public.editions_work.id;


--
-- Name: gsettings_global_var; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.gsettings_global_var (
    id bigint NOT NULL,
    name character varying(128) NOT NULL,
    label character varying(128) NOT NULL,
    value character varying(1024) NOT NULL,
    unit character varying(32) NOT NULL,
    description character varying(1024) NOT NULL,
    global_var_category_id bigint NOT NULL,
    global_var_type_id bigint NOT NULL
);


ALTER TABLE public.gsettings_global_var OWNER TO app_eel;

--
-- Name: gsettings_global_var_category; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.gsettings_global_var_category (
    id bigint NOT NULL,
    name character varying(128) NOT NULL,
    description character varying(1024) NOT NULL
);


ALTER TABLE public.gsettings_global_var_category OWNER TO app_eel;

--
-- Name: gsettings_global_var_category_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.gsettings_global_var_category_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gsettings_global_var_category_id_seq OWNER TO app_eel;

--
-- Name: gsettings_global_var_category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.gsettings_global_var_category_id_seq OWNED BY public.gsettings_global_var_category.id;


--
-- Name: gsettings_global_var_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.gsettings_global_var_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gsettings_global_var_id_seq OWNER TO app_eel;

--
-- Name: gsettings_global_var_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.gsettings_global_var_id_seq OWNED BY public.gsettings_global_var.id;


--
-- Name: gsettings_global_var_type; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.gsettings_global_var_type (
    id bigint NOT NULL,
    name character varying(32) NOT NULL
);


ALTER TABLE public.gsettings_global_var_type OWNER TO app_eel;

--
-- Name: gsettings_global_var_type_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.gsettings_global_var_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gsettings_global_var_type_id_seq OWNER TO app_eel;

--
-- Name: gsettings_global_var_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.gsettings_global_var_type_id_seq OWNED BY public.gsettings_global_var_type.id;


--
-- Name: httpproxy_request; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.httpproxy_request (
    id bigint NOT NULL,
    domain character varying(100) NOT NULL,
    port smallint NOT NULL,
    path character varying(250) NOT NULL,
    date timestamp with time zone NOT NULL,
    querystring character varying(250) NOT NULL
);


ALTER TABLE public.httpproxy_request OWNER TO app_eel;

--
-- Name: httpproxy_request_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.httpproxy_request_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.httpproxy_request_id_seq OWNER TO app_eel;

--
-- Name: httpproxy_request_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.httpproxy_request_id_seq OWNED BY public.httpproxy_request.id;


--
-- Name: httpproxy_response; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.httpproxy_response (
    id bigint NOT NULL,
    request_id bigint NOT NULL,
    status smallint NOT NULL,
    content_type character varying(200) NOT NULL,
    content text NOT NULL
);


ALTER TABLE public.httpproxy_response OWNER TO app_eel;

--
-- Name: httpproxy_response_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.httpproxy_response_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.httpproxy_response_id_seq OWNER TO app_eel;

--
-- Name: httpproxy_response_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.httpproxy_response_id_seq OWNED BY public.httpproxy_response.id;


--
-- Name: menus_cachekey; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.menus_cachekey (
    id integer NOT NULL,
    language character varying(255) NOT NULL,
    site integer NOT NULL,
    key character varying(255) NOT NULL,
    CONSTRAINT menus_cachekey_site_check CHECK ((site >= 0))
);


ALTER TABLE public.menus_cachekey OWNER TO app_eel;

--
-- Name: menus_cachekey_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.menus_cachekey_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.menus_cachekey_id_seq OWNER TO app_eel;

--
-- Name: menus_cachekey_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.menus_cachekey_id_seq OWNED BY public.menus_cachekey.id;


--
-- Name: snippet_snippet; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.snippet_snippet (
    id bigint NOT NULL,
    name character varying(255) NOT NULL,
    html text NOT NULL,
    template character varying(50) NOT NULL
);


ALTER TABLE public.snippet_snippet OWNER TO app_eel;

--
-- Name: snippet_snippet_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.snippet_snippet_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.snippet_snippet_id_seq OWNER TO app_eel;

--
-- Name: snippet_snippet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.snippet_snippet_id_seq OWNED BY public.snippet_snippet.id;


--
-- Name: south_migrationhistory; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.south_migrationhistory (
    id integer NOT NULL,
    app_name character varying(255) NOT NULL,
    migration character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.south_migrationhistory OWNER TO app_eel;

--
-- Name: south_migrationhistory_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.south_migrationhistory_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.south_migrationhistory_id_seq OWNER TO app_eel;

--
-- Name: south_migrationhistory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.south_migrationhistory_id_seq OWNED BY public.south_migrationhistory.id;


--
-- Name: ugc_user_directory; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.ugc_user_directory (
    id bigint NOT NULL,
    name character varying(128) NOT NULL,
    css_class character varying(32) NOT NULL
);


ALTER TABLE public.ugc_user_directory OWNER TO app_eel;

--
-- Name: ugc_user_directory_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.ugc_user_directory_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ugc_user_directory_id_seq OWNER TO app_eel;

--
-- Name: ugc_user_directory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.ugc_user_directory_id_seq OWNED BY public.ugc_user_directory.id;


--
-- Name: ugc_web_user; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.ugc_web_user (
    id bigint NOT NULL,
    affiliations character varying(255) NOT NULL,
    biography text NOT NULL,
    user_id bigint NOT NULL,
    activation_key character varying(128) NOT NULL,
    contactable boolean NOT NULL
);


ALTER TABLE public.ugc_web_user OWNER TO app_eel;

--
-- Name: ugc_web_user_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.ugc_web_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ugc_web_user_id_seq OWNER TO app_eel;

--
-- Name: ugc_web_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.ugc_web_user_id_seq OWNED BY public.ugc_web_user.id;


--
-- Name: ugc_web_user_user_directory; Type: TABLE; Schema: public; Owner: app_eel
--

CREATE TABLE public.ugc_web_user_user_directory (
    id bigint NOT NULL,
    web_user_id bigint NOT NULL,
    user_directory_id bigint NOT NULL
);


ALTER TABLE public.ugc_web_user_user_directory OWNER TO app_eel;

--
-- Name: ugc_web_user_user_directory_id_seq; Type: SEQUENCE; Schema: public; Owner: app_eel
--

CREATE SEQUENCE public.ugc_web_user_user_directory_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ugc_web_user_user_directory_id_seq OWNER TO app_eel;

--
-- Name: ugc_web_user_user_directory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app_eel
--

ALTER SEQUENCE public.ugc_web_user_user_directory_id_seq OWNED BY public.ugc_web_user_user_directory.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.auth_message ALTER COLUMN id SET DEFAULT nextval('public.auth_message_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.auth_user ALTER COLUMN id SET DEFAULT nextval('public.auth_user_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.auth_user_groups ALTER COLUMN id SET DEFAULT nextval('public.auth_user_groups_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_user_user_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.cms_cmsplugin ALTER COLUMN id SET DEFAULT nextval('public.cms_cmsplugin_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.cms_globalpagepermission ALTER COLUMN id SET DEFAULT nextval('public.cms_globalpagepermission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.cms_globalpagepermission_sites ALTER COLUMN id SET DEFAULT nextval('public.cms_globalpagepermission_sites_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.cms_page ALTER COLUMN id SET DEFAULT nextval('public.cms_page_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.cms_page_placeholders ALTER COLUMN id SET DEFAULT nextval('public.cms_page_placeholders_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.cms_pagemoderator ALTER COLUMN id SET DEFAULT nextval('public.cms_pagemoderator_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.cms_pagemoderatorstate ALTER COLUMN id SET DEFAULT nextval('public.cms_pagemoderatorstate_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.cms_pagepermission ALTER COLUMN id SET DEFAULT nextval('public.cms_pagepermission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.cms_placeholder ALTER COLUMN id SET DEFAULT nextval('public.cms_placeholder_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.cms_title ALTER COLUMN id SET DEFAULT nextval('public.cms_title_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.django_site ALTER COLUMN id SET DEFAULT nextval('public.django_site_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.django_template ALTER COLUMN id SET DEFAULT nextval('public.django_template_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.django_template_sites ALTER COLUMN id SET DEFAULT nextval('public.django_template_sites_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_archive ALTER COLUMN id SET DEFAULT nextval('public.editions_archive_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_bib_category ALTER COLUMN id SET DEFAULT nextval('public.editions_bib_category_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_bibliographic_entry ALTER COLUMN id SET DEFAULT nextval('public.editions_bibliographic_entry_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_bibliographic_entry_bib_category ALTER COLUMN id SET DEFAULT nextval('public.editions_bibliographic_entry_bib_category_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_commentary ALTER COLUMN id SET DEFAULT nextval('public.editions_commentary_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_edition ALTER COLUMN id SET DEFAULT nextval('public.editions_edition_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_edition_bibliographic_entry ALTER COLUMN id SET DEFAULT nextval('public.editions_edition_bibliographic_entry_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_edition_translation ALTER COLUMN id SET DEFAULT nextval('public.editions_edition_translation_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_editor ALTER COLUMN id SET DEFAULT nextval('public.editions_editor_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_editor_edition ALTER COLUMN id SET DEFAULT nextval('public.editions_editor_edition_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_eel_edition_status ALTER COLUMN id SET DEFAULT nextval('public.editions_eel_edition_status_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_folio_image ALTER COLUMN id SET DEFAULT nextval('public.editions_folio_image_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_folio_side ALTER COLUMN id SET DEFAULT nextval('public.editions_folio_side_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_glossary_term ALTER COLUMN id SET DEFAULT nextval('public.editions_glossary_term_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_hyparchetype ALTER COLUMN id SET DEFAULT nextval('public.editions_hyparchetype_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_language ALTER COLUMN id SET DEFAULT nextval('public.editions_language_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_manuscript ALTER COLUMN id SET DEFAULT nextval('public.editions_manuscript_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_person ALTER COLUMN id SET DEFAULT nextval('public.editions_person_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_place ALTER COLUMN id SET DEFAULT nextval('public.editions_place_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_resource ALTER COLUMN id SET DEFAULT nextval('public.editions_resource_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_sigla_provenance ALTER COLUMN id SET DEFAULT nextval('public.editions_sigla_provenance_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_text_attribute ALTER COLUMN id SET DEFAULT nextval('public.editions_text_attribute_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_text_attribute_work ALTER COLUMN id SET DEFAULT nextval('public.editions_text_attribute_work_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_topic ALTER COLUMN id SET DEFAULT nextval('public.editions_topic_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_user_comment ALTER COLUMN id SET DEFAULT nextval('public.editions_user_comment_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_version ALTER COLUMN id SET DEFAULT nextval('public.editions_version_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_version_language ALTER COLUMN id SET DEFAULT nextval('public.editions_version_language_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_version_relationship ALTER COLUMN id SET DEFAULT nextval('public.editions_version_relationship_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_version_relationship_type ALTER COLUMN id SET DEFAULT nextval('public.editions_version_relationship_type_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_version_witness ALTER COLUMN id SET DEFAULT nextval('public.editions_version_witness_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_witness ALTER COLUMN id SET DEFAULT nextval('public.editions_witness_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_witness_language ALTER COLUMN id SET DEFAULT nextval('public.editions_witness_language_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_witness_transcription ALTER COLUMN id SET DEFAULT nextval('public.editions_witness_transcription_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_witness_translation ALTER COLUMN id SET DEFAULT nextval('public.editions_witness_translation_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_work ALTER COLUMN id SET DEFAULT nextval('public.editions_work_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.gsettings_global_var ALTER COLUMN id SET DEFAULT nextval('public.gsettings_global_var_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.gsettings_global_var_category ALTER COLUMN id SET DEFAULT nextval('public.gsettings_global_var_category_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.gsettings_global_var_type ALTER COLUMN id SET DEFAULT nextval('public.gsettings_global_var_type_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.httpproxy_request ALTER COLUMN id SET DEFAULT nextval('public.httpproxy_request_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.httpproxy_response ALTER COLUMN id SET DEFAULT nextval('public.httpproxy_response_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.menus_cachekey ALTER COLUMN id SET DEFAULT nextval('public.menus_cachekey_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.snippet_snippet ALTER COLUMN id SET DEFAULT nextval('public.snippet_snippet_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.south_migrationhistory ALTER COLUMN id SET DEFAULT nextval('public.south_migrationhistory_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.ugc_user_directory ALTER COLUMN id SET DEFAULT nextval('public.ugc_user_directory_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.ugc_web_user ALTER COLUMN id SET DEFAULT nextval('public.ugc_web_user_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.ugc_web_user_user_directory ALTER COLUMN id SET DEFAULT nextval('public.ugc_web_user_user_directory_id_seq'::regclass);


--
-- Name: cms_page_placeholders_page_id_598353cf6a0df834_uniq; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.cms_page_placeholders
    ADD CONSTRAINT cms_page_placeholders_page_id_598353cf6a0df834_uniq UNIQUE (page_id, placeholder_id);


--
-- Name: cms_page_placeholders_pkey; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.cms_page_placeholders
    ADD CONSTRAINT cms_page_placeholders_pkey PRIMARY KEY (id);


--
-- Name: cms_placeholder_pkey; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.cms_placeholder
    ADD CONSTRAINT cms_placeholder_pkey PRIMARY KEY (id);


--
-- Name: cms_title_page_id_45628dc0e8a26dd5_uniq; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.cms_title
    ADD CONSTRAINT cms_title_page_id_45628dc0e8a26dd5_uniq UNIQUE (page_id, language);


--
-- Name: idx_153584_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT idx_153584_primary PRIMARY KEY (id);


--
-- Name: idx_153590_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT idx_153590_primary PRIMARY KEY (id);


--
-- Name: idx_153596_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.auth_message
    ADD CONSTRAINT idx_153596_primary PRIMARY KEY (id);


--
-- Name: idx_153605_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT idx_153605_primary PRIMARY KEY (id);


--
-- Name: idx_153611_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT idx_153611_primary PRIMARY KEY (id);


--
-- Name: idx_153617_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT idx_153617_primary PRIMARY KEY (id);


--
-- Name: idx_153623_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT idx_153623_primary PRIMARY KEY (id);


--
-- Name: idx_153627_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.cmsplugin_file
    ADD CONSTRAINT idx_153627_primary PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: idx_153630_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.cmsplugin_googlemap
    ADD CONSTRAINT idx_153630_primary PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: idx_153636_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.cmsplugin_link
    ADD CONSTRAINT idx_153636_primary PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: idx_153642_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.cmsplugin_picture
    ADD CONSTRAINT idx_153642_primary PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: idx_153648_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.cmsplugin_snippetptr
    ADD CONSTRAINT idx_153648_primary PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: idx_153651_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.cmsplugin_text
    ADD CONSTRAINT idx_153651_primary PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: idx_153659_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.cms_cmsplugin
    ADD CONSTRAINT idx_153659_primary PRIMARY KEY (id);


--
-- Name: idx_153665_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.cms_globalpagepermission
    ADD CONSTRAINT idx_153665_primary PRIMARY KEY (id);


--
-- Name: idx_153671_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.cms_globalpagepermission_sites
    ADD CONSTRAINT idx_153671_primary PRIMARY KEY (id);


--
-- Name: idx_153677_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.cms_page
    ADD CONSTRAINT idx_153677_primary PRIMARY KEY (id);


--
-- Name: idx_153683_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.cms_pagemoderator
    ADD CONSTRAINT idx_153683_primary PRIMARY KEY (id);


--
-- Name: idx_153689_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.cms_pagemoderatorstate
    ADD CONSTRAINT idx_153689_primary PRIMARY KEY (id);


--
-- Name: idx_153698_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.cms_pagepermission
    ADD CONSTRAINT idx_153698_primary PRIMARY KEY (id);


--
-- Name: idx_153702_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.cms_pageuser
    ADD CONSTRAINT idx_153702_primary PRIMARY KEY (user_ptr_id);


--
-- Name: idx_153705_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.cms_pageusergroup
    ADD CONSTRAINT idx_153705_primary PRIMARY KEY (group_ptr_id);


--
-- Name: idx_153710_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.cms_title
    ADD CONSTRAINT idx_153710_primary PRIMARY KEY (id);


--
-- Name: idx_153719_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT idx_153719_primary PRIMARY KEY (id);


--
-- Name: idx_153728_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT idx_153728_primary PRIMARY KEY (id);


--
-- Name: idx_153732_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT idx_153732_primary PRIMARY KEY (session_key);


--
-- Name: idx_153740_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.django_site
    ADD CONSTRAINT idx_153740_primary PRIMARY KEY (id);


--
-- Name: idx_153746_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.django_template
    ADD CONSTRAINT idx_153746_primary PRIMARY KEY (id);


--
-- Name: idx_153755_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.django_template_sites
    ADD CONSTRAINT idx_153755_primary PRIMARY KEY (id);


--
-- Name: idx_153761_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_archive
    ADD CONSTRAINT idx_153761_primary PRIMARY KEY (id);


--
-- Name: idx_153767_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_bibliographic_entry
    ADD CONSTRAINT idx_153767_primary PRIMARY KEY (id);


--
-- Name: idx_153776_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_bibliographic_entry_bib_category
    ADD CONSTRAINT idx_153776_primary PRIMARY KEY (id);


--
-- Name: idx_153782_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_bib_category
    ADD CONSTRAINT idx_153782_primary PRIMARY KEY (id);


--
-- Name: idx_153788_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_commentary
    ADD CONSTRAINT idx_153788_primary PRIMARY KEY (id);


--
-- Name: idx_153797_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_edition
    ADD CONSTRAINT idx_153797_primary PRIMARY KEY (id);


--
-- Name: idx_153806_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_edition_bibliographic_entry
    ADD CONSTRAINT idx_153806_primary PRIMARY KEY (id);


--
-- Name: idx_153812_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_edition_translation
    ADD CONSTRAINT idx_153812_primary PRIMARY KEY (id);


--
-- Name: idx_153821_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_editor
    ADD CONSTRAINT idx_153821_primary PRIMARY KEY (id);


--
-- Name: idx_153827_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_editor_edition
    ADD CONSTRAINT idx_153827_primary PRIMARY KEY (id);


--
-- Name: idx_153833_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_eel_edition_status
    ADD CONSTRAINT idx_153833_primary PRIMARY KEY (id);


--
-- Name: idx_153839_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_folio_image
    ADD CONSTRAINT idx_153839_primary PRIMARY KEY (id);


--
-- Name: idx_153848_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_folio_side
    ADD CONSTRAINT idx_153848_primary PRIMARY KEY (id);


--
-- Name: idx_153854_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_glossary_term
    ADD CONSTRAINT idx_153854_primary PRIMARY KEY (id);


--
-- Name: idx_153863_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_hyparchetype
    ADD CONSTRAINT idx_153863_primary PRIMARY KEY (id);


--
-- Name: idx_153870_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_king
    ADD CONSTRAINT idx_153870_primary PRIMARY KEY (person_ptr_id);


--
-- Name: idx_153875_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_language
    ADD CONSTRAINT idx_153875_primary PRIMARY KEY (id);


--
-- Name: idx_153881_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_manuscript
    ADD CONSTRAINT idx_153881_primary PRIMARY KEY (id);


--
-- Name: idx_153890_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_person
    ADD CONSTRAINT idx_153890_primary PRIMARY KEY (id);


--
-- Name: idx_153896_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_place
    ADD CONSTRAINT idx_153896_primary PRIMARY KEY (id);


--
-- Name: idx_153902_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_resource
    ADD CONSTRAINT idx_153902_primary PRIMARY KEY (id);


--
-- Name: idx_153908_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_sigla_provenance
    ADD CONSTRAINT idx_153908_primary PRIMARY KEY (id);


--
-- Name: idx_153914_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_text_attribute
    ADD CONSTRAINT idx_153914_primary PRIMARY KEY (id);


--
-- Name: idx_153920_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_text_attribute_work
    ADD CONSTRAINT idx_153920_primary PRIMARY KEY (id);


--
-- Name: idx_153926_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_topic
    ADD CONSTRAINT idx_153926_primary PRIMARY KEY (id);


--
-- Name: idx_153932_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_user_comment
    ADD CONSTRAINT idx_153932_primary PRIMARY KEY (id);


--
-- Name: idx_153941_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_version
    ADD CONSTRAINT idx_153941_primary PRIMARY KEY (id);


--
-- Name: idx_153950_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_version_language
    ADD CONSTRAINT idx_153950_primary PRIMARY KEY (id);


--
-- Name: idx_153956_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_version_relationship
    ADD CONSTRAINT idx_153956_primary PRIMARY KEY (id);


--
-- Name: idx_153965_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_version_relationship_type
    ADD CONSTRAINT idx_153965_primary PRIMARY KEY (id);


--
-- Name: idx_153974_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_version_witness
    ADD CONSTRAINT idx_153974_primary PRIMARY KEY (id);


--
-- Name: idx_153980_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_witness
    ADD CONSTRAINT idx_153980_primary PRIMARY KEY (id);


--
-- Name: idx_153989_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_witness_language
    ADD CONSTRAINT idx_153989_primary PRIMARY KEY (id);


--
-- Name: idx_153995_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_witness_transcription
    ADD CONSTRAINT idx_153995_primary PRIMARY KEY (id);


--
-- Name: idx_154004_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_witness_translation
    ADD CONSTRAINT idx_154004_primary PRIMARY KEY (id);


--
-- Name: idx_154013_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.editions_work
    ADD CONSTRAINT idx_154013_primary PRIMARY KEY (id);


--
-- Name: idx_154019_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.gsettings_global_var
    ADD CONSTRAINT idx_154019_primary PRIMARY KEY (id);


--
-- Name: idx_154028_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.gsettings_global_var_category
    ADD CONSTRAINT idx_154028_primary PRIMARY KEY (id);


--
-- Name: idx_154037_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.gsettings_global_var_type
    ADD CONSTRAINT idx_154037_primary PRIMARY KEY (id);


--
-- Name: idx_154043_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.httpproxy_request
    ADD CONSTRAINT idx_154043_primary PRIMARY KEY (id);


--
-- Name: idx_154052_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.httpproxy_response
    ADD CONSTRAINT idx_154052_primary PRIMARY KEY (id);


--
-- Name: idx_154061_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.snippet_snippet
    ADD CONSTRAINT idx_154061_primary PRIMARY KEY (id);


--
-- Name: idx_154070_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.ugc_user_directory
    ADD CONSTRAINT idx_154070_primary PRIMARY KEY (id);


--
-- Name: idx_154076_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.ugc_web_user
    ADD CONSTRAINT idx_154076_primary PRIMARY KEY (id);


--
-- Name: idx_154085_primary; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.ugc_web_user_user_directory
    ADD CONSTRAINT idx_154085_primary PRIMARY KEY (id);


--
-- Name: menus_cachekey_pkey; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.menus_cachekey
    ADD CONSTRAINT menus_cachekey_pkey PRIMARY KEY (id);


--
-- Name: south_migrationhistory_pkey; Type: CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.south_migrationhistory
    ADD CONSTRAINT south_migrationhistory_pkey PRIMARY KEY (id);


--
-- Name: cms_cmsplugin_new_placeholder_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX cms_cmsplugin_new_placeholder_id ON public.cms_cmsplugin USING btree (placeholder_id);


--
-- Name: cms_page_limit_visibility_in_menu; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX cms_page_limit_visibility_in_menu ON public.cms_page USING btree (limit_visibility_in_menu);


--
-- Name: cms_page_placeholders_page_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX cms_page_placeholders_page_id ON public.cms_page_placeholders USING btree (page_id);


--
-- Name: cms_page_placeholders_placeholder_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX cms_page_placeholders_placeholder_id ON public.cms_page_placeholders USING btree (placeholder_id);


--
-- Name: cms_placeholder_slot; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX cms_placeholder_slot ON public.cms_placeholder USING btree (slot);


--
-- Name: cms_placeholder_slot_like; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX cms_placeholder_slot_like ON public.cms_placeholder USING btree (slot varchar_pattern_ops);


--
-- Name: idx_153584_name; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE UNIQUE INDEX idx_153584_name ON public.auth_group USING btree (name);


--
-- Name: idx_153590_group_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE UNIQUE INDEX idx_153590_group_id ON public.auth_group_permissions USING btree (group_id, permission_id);


--
-- Name: idx_153590_permission_id_refs_id_5886d21f; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153590_permission_id_refs_id_5886d21f ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: idx_153596_auth_message_user_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153596_auth_message_user_id ON public.auth_message USING btree (user_id);


--
-- Name: idx_153605_auth_permission_content_type_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153605_auth_permission_content_type_id ON public.auth_permission USING btree (content_type_id);


--
-- Name: idx_153605_content_type_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE UNIQUE INDEX idx_153605_content_type_id ON public.auth_permission USING btree (content_type_id, codename);


--
-- Name: idx_153611_username; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE UNIQUE INDEX idx_153611_username ON public.auth_user USING btree (username);


--
-- Name: idx_153617_group_id_refs_id_f116770; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153617_group_id_refs_id_f116770 ON public.auth_user_groups USING btree (group_id);


--
-- Name: idx_153617_user_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE UNIQUE INDEX idx_153617_user_id ON public.auth_user_groups USING btree (user_id, group_id);


--
-- Name: idx_153623_permission_id_refs_id_67e79cb; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153623_permission_id_refs_id_67e79cb ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: idx_153623_user_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE UNIQUE INDEX idx_153623_user_id ON public.auth_user_user_permissions USING btree (user_id, permission_id);


--
-- Name: idx_153636_cmsplugin_link_page_link_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153636_cmsplugin_link_page_link_id ON public.cmsplugin_link USING btree (page_link_id);


--
-- Name: idx_153642_cmsplugin_picture_page_link_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153642_cmsplugin_picture_page_link_id ON public.cmsplugin_picture USING btree (page_link_id);


--
-- Name: idx_153648_cmsplugin_snippetptr_snippet_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153648_cmsplugin_snippetptr_snippet_id ON public.cmsplugin_snippetptr USING btree (snippet_id);


--
-- Name: idx_153659_cms_cmsplugin_language; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153659_cms_cmsplugin_language ON public.cms_cmsplugin USING btree (language);


--
-- Name: idx_153659_cms_cmsplugin_level; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153659_cms_cmsplugin_level ON public.cms_cmsplugin USING btree (level);


--
-- Name: idx_153659_cms_cmsplugin_lft; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153659_cms_cmsplugin_lft ON public.cms_cmsplugin USING btree (lft);


--
-- Name: idx_153659_cms_cmsplugin_parent_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153659_cms_cmsplugin_parent_id ON public.cms_cmsplugin USING btree (parent_id);


--
-- Name: idx_153659_cms_cmsplugin_plugin_type; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153659_cms_cmsplugin_plugin_type ON public.cms_cmsplugin USING btree (plugin_type);


--
-- Name: idx_153659_cms_cmsplugin_rght; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153659_cms_cmsplugin_rght ON public.cms_cmsplugin USING btree (rght);


--
-- Name: idx_153659_cms_cmsplugin_tree_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153659_cms_cmsplugin_tree_id ON public.cms_cmsplugin USING btree (tree_id);


--
-- Name: idx_153665_cms_globalpagepermission_group_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153665_cms_globalpagepermission_group_id ON public.cms_globalpagepermission USING btree (group_id);


--
-- Name: idx_153665_cms_globalpagepermission_user_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153665_cms_globalpagepermission_user_id ON public.cms_globalpagepermission USING btree (user_id);


--
-- Name: idx_153671_globalpagepermission_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE UNIQUE INDEX idx_153671_globalpagepermission_id ON public.cms_globalpagepermission_sites USING btree (globalpagepermission_id, site_id);


--
-- Name: idx_153671_site_id_refs_id_38dfe611; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153671_site_id_refs_id_38dfe611 ON public.cms_globalpagepermission_sites USING btree (site_id);


--
-- Name: idx_153677_cms_page_in_navigation; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153677_cms_page_in_navigation ON public.cms_page USING btree (in_navigation);


--
-- Name: idx_153677_cms_page_level; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153677_cms_page_level ON public.cms_page USING btree (level);


--
-- Name: idx_153677_cms_page_lft; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153677_cms_page_lft ON public.cms_page USING btree (lft);


--
-- Name: idx_153677_cms_page_navigation_extenders; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153677_cms_page_navigation_extenders ON public.cms_page USING btree (navigation_extenders);


--
-- Name: idx_153677_cms_page_parent_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153677_cms_page_parent_id ON public.cms_page USING btree (parent_id);


--
-- Name: idx_153677_cms_page_publication_date; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153677_cms_page_publication_date ON public.cms_page USING btree (publication_date);


--
-- Name: idx_153677_cms_page_publication_end_date; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153677_cms_page_publication_end_date ON public.cms_page USING btree (publication_end_date);


--
-- Name: idx_153677_cms_page_publisher_is_draft; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153677_cms_page_publisher_is_draft ON public.cms_page USING btree (publisher_is_draft);


--
-- Name: idx_153677_cms_page_publisher_state; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153677_cms_page_publisher_state ON public.cms_page USING btree (publisher_state);


--
-- Name: idx_153677_cms_page_reverse_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153677_cms_page_reverse_id ON public.cms_page USING btree (reverse_id);


--
-- Name: idx_153677_cms_page_rght; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153677_cms_page_rght ON public.cms_page USING btree (rght);


--
-- Name: idx_153677_cms_page_site_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153677_cms_page_site_id ON public.cms_page USING btree (site_id);


--
-- Name: idx_153677_cms_page_soft_root; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153677_cms_page_soft_root ON public.cms_page USING btree (soft_root);


--
-- Name: idx_153677_cms_page_tree_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153677_cms_page_tree_id ON public.cms_page USING btree (tree_id);


--
-- Name: idx_153677_publisher_public_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE UNIQUE INDEX idx_153677_publisher_public_id ON public.cms_page USING btree (publisher_public_id);


--
-- Name: idx_153683_cms_pagemoderator_page_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153683_cms_pagemoderator_page_id ON public.cms_pagemoderator USING btree (page_id);


--
-- Name: idx_153683_cms_pagemoderator_user_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153683_cms_pagemoderator_user_id ON public.cms_pagemoderator USING btree (user_id);


--
-- Name: idx_153689_cms_pagemoderatorstate_page_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153689_cms_pagemoderatorstate_page_id ON public.cms_pagemoderatorstate USING btree (page_id);


--
-- Name: idx_153689_cms_pagemoderatorstate_user_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153689_cms_pagemoderatorstate_user_id ON public.cms_pagemoderatorstate USING btree (user_id);


--
-- Name: idx_153698_cms_pagepermission_group_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153698_cms_pagepermission_group_id ON public.cms_pagepermission USING btree (group_id);


--
-- Name: idx_153698_cms_pagepermission_page_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153698_cms_pagepermission_page_id ON public.cms_pagepermission USING btree (page_id);


--
-- Name: idx_153698_cms_pagepermission_user_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153698_cms_pagepermission_user_id ON public.cms_pagepermission USING btree (user_id);


--
-- Name: idx_153702_cms_pageuser_created_by_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153702_cms_pageuser_created_by_id ON public.cms_pageuser USING btree (created_by_id);


--
-- Name: idx_153705_cms_pageusergroup_created_by_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153705_cms_pageusergroup_created_by_id ON public.cms_pageusergroup USING btree (created_by_id);


--
-- Name: idx_153710_cms_title_application_urls; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153710_cms_title_application_urls ON public.cms_title USING btree (application_urls);


--
-- Name: idx_153710_cms_title_has_url_overwrite; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153710_cms_title_has_url_overwrite ON public.cms_title USING btree (has_url_overwrite);


--
-- Name: idx_153710_cms_title_language; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153710_cms_title_language ON public.cms_title USING btree (language);


--
-- Name: idx_153710_cms_title_page_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153710_cms_title_page_id ON public.cms_title USING btree (page_id);


--
-- Name: idx_153710_cms_title_path; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153710_cms_title_path ON public.cms_title USING btree (path);


--
-- Name: idx_153710_cms_title_slug; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153710_cms_title_slug ON public.cms_title USING btree (slug);


--
-- Name: idx_153719_django_admin_log_content_type_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153719_django_admin_log_content_type_id ON public.django_admin_log USING btree (content_type_id);


--
-- Name: idx_153719_django_admin_log_user_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153719_django_admin_log_user_id ON public.django_admin_log USING btree (user_id);


--
-- Name: idx_153728_app_label; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE UNIQUE INDEX idx_153728_app_label ON public.django_content_type USING btree (app_label, model);


--
-- Name: idx_153746_name; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE UNIQUE INDEX idx_153746_name ON public.django_template USING btree (name);


--
-- Name: idx_153755_site_id_refs_id_29215c49; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153755_site_id_refs_id_29215c49 ON public.django_template_sites USING btree (site_id);


--
-- Name: idx_153755_template_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE UNIQUE INDEX idx_153755_template_id ON public.django_template_sites USING btree (template_id, site_id);


--
-- Name: idx_153761_cityname; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE UNIQUE INDEX idx_153761_cityname ON public.editions_archive USING btree (city, name);


--
-- Name: idx_153767_editions_bibliographic_entry_language_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153767_editions_bibliographic_entry_language_id ON public.editions_bibliographic_entry USING btree (language_id);


--
-- Name: idx_153776_editions_bibliographic_entry_bib_category_bib_catego; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153776_editions_bibliographic_entry_bib_category_bib_catego ON public.editions_bibliographic_entry_bib_category USING btree (bib_category_id);


--
-- Name: idx_153776_editions_bibliographic_entry_bib_category_bibliograp; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153776_editions_bibliographic_entry_bib_category_bibliograp ON public.editions_bibliographic_entry_bib_category USING btree (bibliographic_entry_id);


--
-- Name: idx_153782_name; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE UNIQUE INDEX idx_153782_name ON public.editions_bib_category USING btree (name);


--
-- Name: idx_153806_editions_edition_bibliographic_entry_bibliographic_e; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153806_editions_edition_bibliographic_entry_bibliographic_e ON public.editions_edition_bibliographic_entry USING btree (bibliographic_entry_id);


--
-- Name: idx_153806_editions_edition_bibliographic_entry_edition_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153806_editions_edition_bibliographic_entry_edition_id ON public.editions_edition_bibliographic_entry USING btree (edition_id);


--
-- Name: idx_153821_abbreviation; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE UNIQUE INDEX idx_153821_abbreviation ON public.editions_editor USING btree (abbreviation);


--
-- Name: idx_153833_name; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE UNIQUE INDEX idx_153833_name ON public.editions_eel_edition_status USING btree (name);


--
-- Name: idx_153839_filepath; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE UNIQUE INDEX idx_153839_filepath ON public.editions_folio_image USING btree (filepath);


--
-- Name: idx_153848_name; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE UNIQUE INDEX idx_153848_name ON public.editions_folio_side USING btree (name);


--
-- Name: idx_153854_term; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE UNIQUE INDEX idx_153854_term ON public.editions_glossary_term USING btree (term);


--
-- Name: idx_153875_name; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE UNIQUE INDEX idx_153875_name ON public.editions_language USING btree (name);


--
-- Name: idx_153881_shelf_mark; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE UNIQUE INDEX idx_153881_shelf_mark ON public.editions_manuscript USING btree (shelf_mark);


--
-- Name: idx_153890_name; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE UNIQUE INDEX idx_153890_name ON public.editions_person USING btree (name);


--
-- Name: idx_153896_name; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE UNIQUE INDEX idx_153896_name ON public.editions_place USING btree (name);


--
-- Name: idx_153908_name; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE UNIQUE INDEX idx_153908_name ON public.editions_sigla_provenance USING btree (name);


--
-- Name: idx_153914_name; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE UNIQUE INDEX idx_153914_name ON public.editions_text_attribute USING btree (name);


--
-- Name: idx_153920_editions_text_attribute_work_text_attribute_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153920_editions_text_attribute_work_text_attribute_id ON public.editions_text_attribute_work USING btree (text_attribute_id);


--
-- Name: idx_153920_editions_text_attribute_work_work_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153920_editions_text_attribute_work_work_id ON public.editions_text_attribute_work USING btree (work_id);


--
-- Name: idx_153926_name; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE UNIQUE INDEX idx_153926_name ON public.editions_topic USING btree (name);


--
-- Name: idx_153941_standard_abbreviation; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE UNIQUE INDEX idx_153941_standard_abbreviation ON public.editions_version USING btree (standard_abbreviation);


--
-- Name: idx_153956_editions_version_relationship_version_relationship_t; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_153956_editions_version_relationship_version_relationship_t ON public.editions_version_relationship USING btree (version_relationship_type_id);


--
-- Name: idx_153965_name; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE UNIQUE INDEX idx_153965_name ON public.editions_version_relationship_type USING btree (name);


--
-- Name: idx_154013_editions_work_king_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_154013_editions_work_king_id ON public.editions_work USING btree (king_id);


--
-- Name: idx_154013_name; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE UNIQUE INDEX idx_154013_name ON public.editions_work USING btree (name);


--
-- Name: idx_154019_gsettings_global_var_global_var_category_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_154019_gsettings_global_var_global_var_category_id ON public.gsettings_global_var USING btree (global_var_category_id);


--
-- Name: idx_154019_gsettings_global_var_global_var_type_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_154019_gsettings_global_var_global_var_type_id ON public.gsettings_global_var USING btree (global_var_type_id);


--
-- Name: idx_154019_name; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE UNIQUE INDEX idx_154019_name ON public.gsettings_global_var USING btree (name);


--
-- Name: idx_154028_name; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE UNIQUE INDEX idx_154028_name ON public.gsettings_global_var_category USING btree (name);


--
-- Name: idx_154037_name; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE UNIQUE INDEX idx_154037_name ON public.gsettings_global_var_type USING btree (name);


--
-- Name: idx_154052_request_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE UNIQUE INDEX idx_154052_request_id ON public.httpproxy_response USING btree (request_id);


--
-- Name: idx_154061_name; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE UNIQUE INDEX idx_154061_name ON public.snippet_snippet USING btree (name);


--
-- Name: idx_154070_name; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE UNIQUE INDEX idx_154070_name ON public.ugc_user_directory USING btree (name);


--
-- Name: idx_154076_user_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE UNIQUE INDEX idx_154076_user_id ON public.ugc_web_user USING btree (user_id);


--
-- Name: idx_154085_ugc_web_user_user_directory_user_directory_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_154085_ugc_web_user_user_directory_user_directory_id ON public.ugc_web_user_user_directory USING btree (user_directory_id);


--
-- Name: idx_154085_ugc_web_user_user_directory_web_user_id; Type: INDEX; Schema: public; Owner: app_eel
--

CREATE INDEX idx_154085_ugc_web_user_user_directory_web_user_id ON public.ugc_web_user_user_directory USING btree (web_user_id);


--
-- Name: new_placeholder_id_refs_id_df6bb944; Type: FK CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.cms_cmsplugin
    ADD CONSTRAINT new_placeholder_id_refs_id_df6bb944 FOREIGN KEY (placeholder_id) REFERENCES public.cms_placeholder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: page_id_refs_id_b22baae5; Type: FK CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.cms_page_placeholders
    ADD CONSTRAINT page_id_refs_id_b22baae5 FOREIGN KEY (page_id) REFERENCES public.cms_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: placeholder_id_refs_id_b0df4960; Type: FK CONSTRAINT; Schema: public; Owner: app_eel
--

ALTER TABLE ONLY public.cms_page_placeholders
    ADD CONSTRAINT placeholder_id_refs_id_b0df4960 FOREIGN KEY (placeholder_id) REFERENCES public.cms_placeholder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

