CREATE TABLE IF NOT EXISTS user (
   id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
   futures_account TEXT NOT NULL,
	 futures_password TEXT NOT NULL,
	 tq_account TEXT NOT NULL,
	 tq_password TEXT NOT NULL,
	 account_type INT NOT NULL,
	 disable INT NOT NULL,
	 created_at TEXT NOT NULL DEFAULT (DATETIME('now', 'localtime')),
	 updated_at TEXT NOT NULL DEFAULT (DATETIME('now', 'localtime'))
);

CREATE TRIGGER IF NOT EXISTS trigger_user_updated_at AFTER UPDATE ON user
BEGIN
    UPDATE user SET updated_at = DATETIME('now', 'localtime') WHERE rowid == NEW.rowid;
END;