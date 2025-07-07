from sqlitedict import SqliteDict

DB_PATH = "history.sqlite"

def save_history(entry_id, data):
    with SqliteDict(DB_PATH) as db:
        db[entry_id] = data
        db.commit()

def get_all_history():
    with SqliteDict(DB_PATH) as db:
        return dict(db)
