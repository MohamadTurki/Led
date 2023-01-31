import sqlite3
conn = sqlite3.connect('database.db')

c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    some_column TEXT
)
""")

c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user.username, user.password))

conn.close()
