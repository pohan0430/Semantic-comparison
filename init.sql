CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS Users (
    username VARCHAR PRIMARY KEY,
    password VARCHAR(64)
);

INSERT INTO Users (username, password) VALUES ('admin', 'admin');
