CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL,
    full_name TEXT,
    email TEXT,
    birth_year INTEGER,
    gender boolean, -- 1: male, 0: female
    height INTEGER,
    weight INTEGER,
    married boolean,
    work INTEGER, -- stroke (never worked, private, self-employed, gov, children) 
    residence boolean, -- 0: rural, 1: urban
    smoke INTEGER, -- 0: unknown, 1: never, 2: former, 3: current
    pregnancies INTEGER,
    -- cp INTEGER, -- 1: typical angina, 2: atypical angina, 3: non-anginal pain, 4: asymptomatic
    exng boolean,
    heart_disease boolean
);

CREATE UNIQUE INDEX username ON users (username);

CREATE TABLE locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL,
);

CREATE TABLE appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER NOT NULL,
    time INTEGER NOT NULL,
    location_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (location_id) REFERENCES locations (id)
);
