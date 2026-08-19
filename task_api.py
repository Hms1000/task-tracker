from fastapi import FastAPI
from sqlmodel import SQLModel, Field, create_engine, Session, select
class Task(SQLModel, table=True):
     id: int | None = Field(default=None, primary_key=True)
     title: str = Field(unique=True)
     priority: str
     done: bool = False
     due_date: str | None = None
     frequency: str | None = None

engine = create_engine("sqlite:///tracker.db")
SQLModel.metadata.create_all(engine)

app = FastAPI() #fastapi client

@app.get("/tasks") # get endpoint used to list all tasks
def list_tasks():
      with Session(engine) as session:
           return session.exec(select(Task)).all()

@app.post("/tasks")
def create_task(task: Task):
     with Session(engine) as session:
          session.add(task)
          session.commit()
          session.refresh(task)
          return task
    

@app.delete("/tasks/{title}")
def delete_task(title: str):
     with Session(engine) as session:
          statement = select(Task).where(Task.title == title)
          task = session.exec(statement).first()
          if not task:
               return {"message": "Task not found"}
          session.delete(task)
          session.commit()
          return {"message": f"Deleted {title}"}

@app.get("/tasks/filter")
def filter_tasks(priority: str):
     with Session(engine) as session:
          statement = select(Task).where(Task.priority == priority)
          return session.exec(statement).all()

@app.put("/tasks/{title}")
def update_task(title: str, updated:Task):
     with Session(engine) as session:
          statement = select(Task).where(Task.title == title)
          task = session.exec(statement).first()
          if not task:
               return {"message": "Task not found"}
          task.priority = updated.priority
          task.done = updated.done
          task.due_date = updated.due_date
          task.frequency = updated.frequency
          session.add(task)
          session.commit()
          return task