import sqlite3

conn = sqlite3.connect("database.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);
""")

cursor.execute("""
CREATE TABLE expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    amount REAL NOT NULL,
    category TEXT DEFAULT 'Lainnya',
    date TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id)
);
""")

nama_input = 'ivan'
password_input = 'Azmah986@'

cursor.execute(
    "INSERT INTO users (username, password_hash) VALUES (?, ?)", (nama_input, password_input)
)

conn.commit()

cursor.execute("SELECT * FROM users")
all_users = cursor.fetchall()

print('---- User Data ----')
for id_user, username, password in all_users:
    print(f"ID: {id_user} | Username: {username} | Password: {password}")


conn.close()