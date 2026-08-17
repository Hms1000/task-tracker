from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI() #fastapi client

def get_connection(): #getting db connection and creating a cursor
    conn = sqlite3.connect("tracker.db")
    conn.row_factory = sqlite3.Row
    return conn

setup_conn = get_connection()
setup_cursor = setup_conn.cursor()


# creating tasks table
setup_cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
    title TEXT UNIQUE,
    priority TEXT,
    done BOOLEAN,
    due_date TEXT,
    frequency TEXT
    )
""")

setup_conn.commit()
setup_conn.close()

@app.get("/tasks") # get endpoint used to list all tasks
def list_tasks():
      conn = get_connection()
      cursor = conn.cursor()
      cursor.execute("SELECT * FROM tasks")
      rows = cursor.fetchall()
      conn.close()

      return [dict(row) for row in rows] #converting sqlite3.Row into a real Python dict