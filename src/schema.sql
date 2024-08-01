CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL,
    age INTEGER,
    gender boolean,
    hight_cm INTEGER,
    weight_g INTEGER,
    married boolean,
    work INTEGER,
    residence boolean,
    smoke INTEGER,
    pregnancies INTEGER,
    cp INTEGER,
    exng boolean,
    heart_disease boolean
);

CREATE UNIQUE INDEX username ON users (username);