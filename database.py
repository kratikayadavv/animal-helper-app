import sqlite3

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

print("Database created!")