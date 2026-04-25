import sqlite3
def init_db():
    conn = sqlite3.connect("animals_v3.db")
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS cases")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        animal TEXT,
        location TEXT,
        description TEXT,
        image TEXT,
        helper_name TEXT,
        helper_contact TEXT        
)
""")

conn.commit()
conn.close()

init_db()
print("Database created!")
