CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS Users (
    username VARCHAR PRIMARY KEY,
    password VARCHAR(64)
);

INSERT INTO Users (username, password) VALUES ('admin', 'admin');

CREATE TABLE News_Embedding (
    news_id INTEGER PRIMARY KEY,
    title TEXT,
    content TEXT,
    cat_lv1 TEXT,
    cat_lv2 TEXT,
    keywords TEXT,
    url TEXT,
    date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    img TEXT,
    audience INTEGER,
    embedding VECTOR(512)
);

COPY news_embedding FROM '/csv/news_embedding.csv' DELIMITER ',' CSV HEADER;
