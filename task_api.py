from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI() #fastapi client

def get_connection(): #getting db connection and creating a cursor
    with sqlite3.connect("tracker.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            return cursor, conn

cursor, conn = get_connection()

# creating tasks table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
    title TEXT UNIQUE,
    priority TEXT,
    done BOOLEAN,
    due_date TEXT,
    frequency TEXT
    )
""")

conn.commit()

@app.get("/tasks") # get endpoint used to list all tasks
def list_tasks():
      cursor.execute("SELECT * FROM tasks")
      rows = cursor.fetchall()
      conn.close()

      return [dict(row) for row in rows] #converting sqlite3.Row into a real Python dict