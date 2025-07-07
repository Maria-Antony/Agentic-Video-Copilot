import os
import json
from datetime import datetime

SESSIONS_DIR = "sessions"
os.makedirs(SESSIONS_DIR, exist_ok=True)

def save_session_to_disk(context):
    filename = f"{datetime.utcnow().isoformat().replace(':','-')}.json"
    filepath = os.path.join(SESSIONS_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(context, f, ensure_ascii=False, indent=2)
    return filepath

def load_sessions_from_disk():
    sessions = []
    for filename in sorted(os.listdir(SESSIONS_DIR)):
        if filename.endswith(".json"):
            with open(os.path.join(SESSIONS_DIR, filename), "r", encoding="utf-8") as f:
                session = json.load(f)
                sessions.append(session)
    return sessions[::-1]  # Newest first
