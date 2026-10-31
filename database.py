"""SQLite layer for the Railway AI project."""
import os
import sqlite3
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "database", "passengers.db")
FACES_DIR = os.path.join(BASE, "faces")
TICKETS_DIR = os.path.join(BASE, "tickets")


def connect():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)


def create_database():
    os.makedirs(FACES_DIR, exist_ok=True)
    os.makedirs(TICKETS_DIR, exist_ok=True)
    con = connect()
    con.execute("""CREATE TABLE IF NOT EXISTS passengers(
        ticket_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        seat TEXT NOT NULL,
        train TEXT,
        face_file TEXT NOT NULL,
        created TEXT)""")
    con.execute("""CREATE TABLE IF NOT EXISTS logs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id TEXT,
        result TEXT,
        score REAL,
        time TEXT)""")
    con.commit()
    con.close()


def add_passenger(ticket_id, name, seat, train, face_file):
    """Returns True on success, False if the ticket ID already exists."""
    con = connect()
    try:
        con.execute("INSERT INTO passengers VALUES (?,?,?,?,?,?)",
                    (ticket_id, name, seat, train, face_file, now()))
        con.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        con.close()


def get_passenger(ticket_id):
    con = connect()
    row = con.execute(
        "SELECT ticket_id,name,seat,train,face_file,created "
        "FROM passengers WHERE ticket_id=?", (ticket_id,)).fetchone()
    con.close()
    return row


def list_passengers():
    con = connect()
    rows = con.execute(
        "SELECT ticket_id,name,seat,train,created FROM passengers "
        "ORDER BY created DESC").fetchall()
    con.close()
    return rows


def delete_passenger(ticket_id):
    p = get_passenger(ticket_id)
    if not p:
        return
    for f in (p[4], os.path.join(TICKETS_DIR, f"{ticket_id}.png")):
        if f and os.path.exists(f):
            os.remove(f)
    con = connect()
    con.execute("DELETE FROM passengers WHERE ticket_id=?", (ticket_id,))
    con.commit()
    con.close()


def add_log(ticket_id, result, score=None):
    con = connect()
    con.execute("INSERT INTO logs(ticket_id,result,score,time) VALUES (?,?,?,?)",
                (ticket_id, result, score, now()))
    con.commit()
    con.close()


def list_logs():
    con = connect()
    rows = con.execute(
        "SELECT id,ticket_id,result,score,time FROM logs ORDER BY id DESC"
    ).fetchall()
    con.close()
    return rows


def stats():
    con = connect()
    out = {
        "passengers": con.execute("SELECT COUNT(*) FROM passengers").fetchone()[0],
        "checks": con.execute("SELECT COUNT(*) FROM logs").fetchone()[0],
    }
    for r in ("MATCH", "MISMATCH", "UNABLE TO VERIFY", "NOT FOUND"):
        out[r] = con.execute("SELECT COUNT(*) FROM logs WHERE result=?",
                             (r,)).fetchone()[0]
    con.close()
    return out


def wipe_all():
    """Delete ALL test data (biometric photos, tickets, records)."""
    for d in (FACES_DIR, TICKETS_DIR):
        if os.path.isdir(d):
            for f in os.listdir(d):
                os.remove(os.path.join(d, f))
    con = connect()
    con.execute("DELETE FROM passengers")
    con.execute("DELETE FROM logs")
    con.commit()
    con.close()


def now():
    return datetime.now().isoformat(timespec="seconds")


create_database()

if __name__ == "__main__":
    print("Passenger database created successfully!")
    print("Location:", DB_PATH)
