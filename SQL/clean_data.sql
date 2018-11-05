ALTER TABLE page 
  DROP INDEX page_random,
  DROP INDEX page_len,
  DROP INDEX page_redirect_namespace_len,
  DROP COLUMN page_restrictions,
  DROP COLUMN page_counter,
  DROP COLUMN page_is_redirect,
  DROP COLUMN page_is_new,
  DROP COLUMN page_random,
  DROP COLUMN page_links_updated,
  DROP COLUMN page_len,
  DROP COLUMN page_no_title_convert,
  DROP COLUMN page_content_model,
  DROP COLUMN page_lang;

CREATE INDEX p_title ON page (page_title ASC);


ALTER TABLE categorylinks 
  DROP INDEX cl_sortkey,
  DROP INDEX cl_collation_ext,
  DROP COLUMN cl_sortkey,
  DROP COLUMN cl_sortkey_prefix,
  DROP COLUMN cl_collation;

CREATE INDEX cl_sortkey ON categorylinks (cl_to ASC, cl_type ASC, cl_from ASC);


CREATE INDEX pl_title ON pagelinks (pl_title ASC);