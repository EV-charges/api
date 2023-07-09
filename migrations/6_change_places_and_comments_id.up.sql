ALTER TABLE places ALTER COLUMN id TYPE bigint;
ALTER TABLE comments ALTER COLUMN comment_id TYPE VARCHAR(50);
ALTER TABLE places_sources ALTER COLUMN inner_id TYPE bigint;