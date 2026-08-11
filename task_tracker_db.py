import sqlite3

# connecting to the database and creating a cursor
conn = sqlite3.connect("tracker.db")
cursor = conn.cursor()

# creating a table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
    title TEXT UNIQUE,
    priority TEXT,
    done BOOLEAN,
    due_date TEXT,
    frequency TEXT
    )
""")
# adding actual data to the table
cursor.execute(
    "INSERT INTO tasks (title, priority, done, due_date, frequency) VALUES (?, ?, ?, ?, ?)",
    ("Dune", "low", 0, "June 30", "weekly"),
      )

cursor.execute("SELECT * FROM tasks")

rows = cursor.fetchall()
print(rows)

conn.commit()