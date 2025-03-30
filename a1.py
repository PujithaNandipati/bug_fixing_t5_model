import sqlite3

# Connect to SQLite database (or create one if it doesn't exist)
conn = sqlite3.connect("bug_fixing.db", check_same_thread=False)
cursor = conn.cursor()

# Create a table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS bug_fixes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    buggy_code TEXT,
    fixed_code TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

def save_to_db(buggy_code, fixed_code):
    """Save input and output to database."""
    cursor.execute("INSERT INTO bug_fixes (buggy_code, fixed_code) VALUES (?, ?)", (buggy_code, fixed_code))
    conn.commit()
