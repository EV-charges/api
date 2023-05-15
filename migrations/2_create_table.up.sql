CREATE TABLE IF NOT EXISTS places (
    id SERIAL PRIMARY KEY,
    location geography(POINT),
    name VARCHAR(100) NOT NULL,
    city VARCHAR(30),
    street VARCHAR(70)
);

CREATE TABLE IF NOT EXISTS places_sources (
    id SERIAL PRIMARY KEY,
    place_id INTEGER NOT NULL,
    inner_id INTEGER NOT NULL,
    source VARCHAR(30) NOT NULL,
    FOREIGN KEY (place_id) REFERENCES places (id) ON DELETE CASCADE
);