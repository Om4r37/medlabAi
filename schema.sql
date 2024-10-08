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
    work INTEGER, -- (0: never worked, 1: private, 2: self-employed, 3: gov, 4: children)
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
    done boolean DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (location_id) REFERENCES locations (id),
    FOREIGN KEY (test_id) REFERENCES tests (id)
);

CREATE TABLE results_fields (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    appointment_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    value TEXT NOT NULL,
    FOREIGN KEY (appointment_id) REFERENCES appointments (id)
);

CREATE TABLE stats (
    name TEXT,
    value INTEGER Default 0
);

-- Indexes for frequently queried columns
CREATE INDEX idx_appointments_user_id ON appointments (user_id);
CREATE INDEX idx_appointments_location_id ON appointments (location_id);
CREATE INDEX idx_appointments_test_id ON appointments (test_id);
CREATE INDEX idx_results_fields_appointment_id ON results_fields (appointment_id);
