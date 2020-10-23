-- Registrations

CREATE TABLE IF NOT EXISTS registrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event INTEGER NOT NULL,
    name VARCHAR(128) NOT NULL,
    time DATETIME NOT NULL,
    admin BOOLEAN NOT NULL,
    deleted BOOLEAN NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_registrations_event_name ON registrations (event, name);

-- Quiz

CREATE TABLE IF NOT EXISTS quiz_participants (
    quiz VARCHAR(128) NOT NULL,
    name VARCHAR(128) NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_quiz_participants_quiz_name ON quiz_participants (quiz, name);

CREATE TABLE IF NOT EXISTS quiz_answers (
    id VARCHAR(32) PRIMARY KEY,
    quiz VARCHAR(128) NOT NULL,
    correct INTEGER NOT NULL,
    answers TEXT NOT NULL
);
