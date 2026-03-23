import sqlite3

DB_NAME = "vault.db"

def setup_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vault (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def display_credentials(rows):
    if not rows:
        print("  (no results)")
    else:
        for row in rows:
            print(f"  {row[1]:<14} | {row[2]:<12} | {row[3]}")

# ── TODO 1 ──────────────────────────────────────────────────────────────────
def add_credential(website, username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO vault (website, username, password) VALUES (?, ?, ?)",
        (website, username, password)
    )
    conn.commit()
    conn.close()

# ── TODO 2 ──────────────────────────────────────────────────────────────────
def get_all_credentials():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vault ORDER BY website ASC")
    rows = cursor.fetchall()
    conn.close()
    return rows

# ── TODO 3 ──────────────────────────────────────────────────────────────────
def find_credential(website):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vault WHERE website = ?", (website,))
    rows = cursor.fetchall()
    conn.close()
    return rows

# ── MAIN ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    setup_database()

    print("=" * 60)
    print("  PASSWORD VAULT")
    print("=" * 60)

    print("\n--- Adding Credentials ---")
    credentials = [
        ("github.com",  "admin",        "s3cur3P@ss"),
        ("google.com",  "maziar@gmail", "MyP@ssw0rd"),
        ("netflix.com", "maziar",       "N3tfl1x!"),
        ("github.com",  "work_user",    "W0rkP@ss!"),
    ]
    for website, username, password in credentials:
        add_credential(website, username, password)
        print(f"  Saved: {website}" + (" (work)" if username == "work_user" else ""))

    print("\n--- All Credentials ---")
    display_credentials(get_all_credentials())

    print("\n--- Search for 'github.com' ---")
    display_credentials(find_credential("github.com"))

    print("\n--- Search for 'spotify.com' ---")
    display_credentials(find_credential("spotify.com"))

    print("\n" + "=" * 60)