import sqlite3

DB_PATH = "data/predictions.db"

class PredictionLogger:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            text TEXT NOT NULL,
            api_sentiment TEXT,
            api_score REAL,
            model_label TEXT NOT NULL,
            model_score REAL NOT NULL,
            model_version TEXT NOT NULL
        )
        """)
        conn.commit()
        conn.close()

    def log(self, ticker, text, api_sentiment, api_score, model_label, model_score, model_version):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
            INSERT INTO predictions
            (ticker, text, api_sentiment, api_score, model_label, model_score, model_version)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (ticker, text, api_sentiment, api_score, model_label, model_score, model_version))
        conn.commit()
        conn.close()