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
    exng boolean,
    heart_disease boolean
);

CREATE UNIQUE INDEX username ON users (username);

CREATE TABLE locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL
);

CREATE TABLE tests (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    duration INTEGER NOT NULL, -- in minutes
    name TEXT NOT NULL
);

CREATE TABLE prerequisites (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL,
    test_id INTEGER NOT NULL,
    FOREIGN KEY (test_id) REFERENCES tests (id)
);

CREATE TABLE appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    time TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    location_id INTEGER NOT NULL,
    test_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (location_id) REFERENCES locations (id),
    FOREIGN KEY (test_id) REFERENCES tests (id)
);

CREATE TABLE stats (
    current_appointments INTEGER Default 0,
    total_results INTEGER Default 0,
    users_count INTEGER Default 0,
    male INTEGER Default 0,
    female INTEGER Default 0,
    married INTEGER Default 0,
    current_smokers INTEGER Default 0,
    former_smokers INTEGER Default 0,
    never_smokers INTEGER Default 0,
    heart_disease INTEGER Default 0,
    exng INTEGER Default 0,
    rural INTEGER Default 0,
    urban INTEGER Default 0,
    private_work INTEGER Default 0,
    self_employed INTEGER Default 0,
    gov_work INTEGER Default 0,
    children INTEGER Default 0,
    ages_0_15 INTEGER Default 0,
    ages_16_30 INTEGER Default 0,
    ages_31_45 INTEGER Default 0,
    ages_46_60 INTEGER Default 0,
    ages_61_75 INTEGER Default 0,
    ages_76_ INTEGER Default 0
);