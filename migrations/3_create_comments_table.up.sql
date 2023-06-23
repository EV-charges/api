CREATE TABLE IF NOT EXISTS comments (
    id SERIAL PRIMARY KEY,
    place_id INT NOT NULL,
    comment_id INT NOT NULL,
    author VARCHAR(150),
    text TEXT,
    publication_date TIMESTAMP,
    source TEXT NOT NULL,
    FOREIGN KEY (place_id) REFERENCES places (id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP


);

-- TODO: CONSTRAINT comment_id_source_unique UNIQUE (comment_id, source) ALTER TABLE!!!!
