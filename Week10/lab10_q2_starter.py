import sqlite3
from datetime import datetime

DB_NAME = "login_attempts.db"

def setup_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS login_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            success INTEGER NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# ── TODO 1 ──────────────────────────────────────────────────────────────────
def record_attempt(username, success):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO login_attempts (username, success, timestamp) VALUES (?, ?, ?)",
        (username, success, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    conn.close()

# ── TODO 2 ──────────────────────────────────────────────────────────────────
def get_failed_attempts(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM login_attempts WHERE username = ? AND success = 0",
        (username,)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows

# ── TODO 3 ──────────────────────────────────────────────────────────────────
def count_failures_per_user():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT username, COUNT(*) FROM login_attempts WHERE success = 0 GROUP BY username"
    )
    rows = cursor.fetchall()
    conn.close()
    return rows

# ── TODO 4 ──────────────────────────────────────────────────────────────────
def delete_old_attempts(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM login_attempts WHERE username = ?", (username,))
    deleted = cursor.rowcount
    conn.commit()
    conn.close()
    return deleted

# ── MAIN ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    setup_database()

    print("=" * 60)
    print("  LOGIN ATTEMPT TRACKER")
    print("=" * 60)

    print("\n--- Recording Login Attempts ---")
    attempts = [
        ("admin", True),
        ("admin", False),
        ("admin", False),
        ("admin", False),
        ("guest", True),
        ("guest", False),
        ("root",  False),
        ("root",  False),
        ("root",  False),
        ("root",  False),
    ]
    for username, success in attempts:
        record_attempt(username, success)
        label = "success" if success else "FAILED"
        print(f"  Recorded: {username} ({label})")

    print("\n--- Failed Attempts for 'admin' ---")
    for row in get_failed_attempts("admin"):
        print(f"  {row[1]:<8} | FAILED  | {row[3]}")

    print("\n--- Failure Counts ---")
    for username, count in count_failures_per_user():
        warning = f"  ⚠ {username} has {count} failed attempts — possible brute-force!" if count >= 4 else ""
        print(f"  {username:<12}{count} failed attempts{warning}")

    print("\n--- Reset 'root' account (delete all attempts) ---")
    deleted = delete_old_attempts("root")
    print(f"  Deleted {deleted} records for root")

    print("\n--- Failure Counts (after reset) ---")
    for username, count in count_failures_per_user():
        print(f"  {username:<12}{count} failed attempts")

    print("\n" + "=" * 60)