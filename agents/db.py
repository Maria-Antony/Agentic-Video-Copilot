import sqlite3
import json
from datetime import datetime

DB_FILE = "mcp_sessions.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url_or_file TEXT,
            summary TEXT,
            resources TEXT,
            qa_log TEXT,
            language TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_session(context):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        INSERT INTO sessions (url_or_file, summary, resources, qa_log, language, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        context["url_or_file"],
        context["summary"],
        json.dumps(context["resources"], ensure_ascii=False),
        json.dumps(context["qa_log"], ensure_ascii=False),
        context["language"],
        datetime.utcnow().isoformat()
    ))
    conn.commit()
    conn.close()

def load_all_sessions():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT * FROM sessions ORDER BY id DESC')
    rows = c.fetchall()
    conn.close()

    sessions = []
    for row in rows:
        sessions.append({
            "url_or_file": row[1],
            "summary": row[2],
            "resources": row[3],
            "qa_log": json.loads(row[4]),
            "language": row[5],
            "created_at": row[6]
        })
    return sessions
