CREATE TABLE IF NOT EXISTS registrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event INTEGER NOT NULL,
    name VARCHAR(128) NOT NULL,
    time DATETIME NOT NULL,
    admin BOOLEAN NOT NULL,
    deleted BOOLEAN NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_registrations_event_name ON registrations (event, name);
