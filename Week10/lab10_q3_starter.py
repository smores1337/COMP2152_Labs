import sqlite3
import unittest

DB_NAME = "audit_log.db"

def setup_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event TEXT NOT NULL,
            severity TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    # Seed sample data (clear first to avoid duplicates on re-runs)
    cursor.execute("DELETE FROM audit_log")
    sample_events = [
        ("Unauthorized access attempt",  "HIGH",   "2026-03-10 08:15:00"),
        ("Port scan detected",           "HIGH",   "2026-03-11 09:30:00"),
        ("SQL injection attempt",        "HIGH",   "2026-03-12 10:45:00"),
        ("Failed login x3",             "MEDIUM", "2026-03-13 11:00:00"),
        ("Config file changed",          "MEDIUM", "2026-03-14 12:20:00"),
        ("New user created",             "LOW",    "2026-03-15 13:35:00"),
        ("Password changed",             "LOW",    "2026-03-16 14:50:00"),
        ("Routine backup completed",     "LOW",    "2026-03-17 15:05:00"),
        ("Service restarted",            "LOW",    "2026-03-18 16:20:00"),
        ("Disk usage above 90%",         "MEDIUM", "2026-03-19 17:35:00"),
    ]
    cursor.executemany(
        "INSERT INTO audit_log (event, severity, timestamp) VALUES (?, ?, ?)",
        sample_events
    )
    conn.commit()
    conn.close()

# ── TODO 1 ──────────────────────────────────────────────────────────────────
def get_events_by_severity(severity):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM audit_log WHERE severity = ?", (severity,))
    rows = cursor.fetchall()
    conn.close()
    return rows

# ── TODO 2 ──────────────────────────────────────────────────────────────────
def get_recent_events(limit):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM audit_log ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows

# ── TODO 3 ──────────────────────────────────────────────────────────────────
def count_by_severity():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT severity, COUNT(*) FROM audit_log GROUP BY severity ORDER BY COUNT(*) DESC"
    )
    rows = cursor.fetchall()
    conn.close()
    return rows

# ── TODO 4 ──────────────────────────────────────────────────────────────────
def safe_query(query):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        conn.close()

# ── UNIT TESTS ───────────────────────────────────────────────────────────────
class TestAuditLog(unittest.TestCase):

    def test_high_severity(self):
        rows = get_events_by_severity("HIGH")
        self.assertEqual(len(rows), 3)

    def test_recent_events(self):
        rows = get_recent_events(5)
        self.assertEqual(len(rows), 5)

    def test_count(self):
        results = count_by_severity()
        self.assertIn(("HIGH", 3), results)

    def test_safe_bad_query(self):
        result = safe_query("SELECT * FROM fake_table")
        self.assertEqual(result, [])

# ── MAIN ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    setup_database()

    print("=" * 60)
    print("  SECURITY AUDIT LOG")
    print("=" * 60)

    print("\n--- HIGH Severity Events ---")
    for row in get_events_by_severity("HIGH"):
        print(f"  [{row[3]}] {row[2]:<8} | {row[1]}")

    print("\n--- 5 Most Recent Events ---")
    for row in get_recent_events(5):
        print(f"  [{row[3]}] {row[2]:<8} | {row[1]}")

    print("\n--- Event Counts by Severity ---")
    for severity, count in count_by_severity():
        print(f"  {severity:<8} {count} events")

    print("\n--- Safe Query Test (bad table) ---")
    safe_query("SELECT * FROM fake_table")

    print("\n--- Running Unit Tests ---")
    unittest.main(argv=[""], verbosity=2, exit=False)