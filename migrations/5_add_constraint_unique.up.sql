ALTER TABLE comments
ADD CONSTRAINT comment_id_source_unique UNIQUE (comment_id, source);
