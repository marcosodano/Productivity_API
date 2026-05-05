import sqlite3

# 1. Connect to the database
conn = sqlite3.connect("vault.db", check_same_thread=False)

# 2. Create a cursor
cursor = conn.cursor()


# 3. Define the Table setup
def setup_database():
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dish_name TEXT NOT NULL,   
            filename TEXT NOT NULL,
            file_type TEXT NOT NULL
            )
        """)
    conn.commit()


# 4. Run the setup as soon as the file is opened
setup_database()
