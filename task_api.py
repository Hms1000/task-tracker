from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

class TaskIn(BaseModel):
     title: str
     priority: str
     done: bool = False
     due_date: str | None = None
     frequency: str | None = None

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

@app.post("/tasks")
def create_task(task: TaskIn):
     conn = get_connection()
     cursor = conn.cursor()

     cursor.execute(
          "INSERT INTO tasks (title, priority, done, due_date, frequency) VALUES (?, ?, ?, ?, ?)",
          (task.title, task.priority, task.done, task.due_date, task.frequency)
                    )
     conn.commit()
     conn.close()

     return {"message": f"Task '{task.title}' added"}

@app.delete("/tasks/{title}")
def delete_task(title: str):
     conn = get_connection()
     cursor = conn.cursor()

     cursor.execute(
          "DELETE FROM tasks WHERE title = ?",
          (title,)
     )

     conn.commit()
     conn.close()

     return {"message": f"Deleted {title}"}

@app.get("/tasks/filter")
def filter_tasks(priority: str):
     conn = get_connection()
     cursor = conn.cursor()
     cursor.execute("SELECT * FROM tasks WHERE priority = ?", (priority,))
     rows = cursor.fetchall()
     conn.close()

     return [dict(row) for row in rows]

@app.put("/tasks/{title}")
def update_task(title: str, task:TaskIn):
     conn = get_connection()
     cursor = conn.cursor()

     cursor.execute(
          "UPDATE tasks SET priority = ?, done = ?, due_date = ?, frequency = ? WHERE title = ?",
          (task.priority, task.done, task.due_date, task.frequency, title)
     )
     conn.commit()
     conn.close()

     return {"message": f"Updated {title}"}