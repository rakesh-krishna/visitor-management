DROP TABLE IF EXISTS posts;

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT (datetime('now','localtime')),
    username TEXT NOT NULL,
    reason TEXT NOT NULL,
    whom_to_meet TEXT,
    exit TIMESTAMP
);
