from fastapi import FastAPI, HTTPException
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from sqlmodel import SQLModel, Field, create_engine, Session
class Task(SQLModel, table=True):
     __tablename__ = "tasks"
     id: int | None = Field(default=None, primary_key=True)
     title: str = Field(unique=True)
     priority: str
     done: bool = False
     due_date: str | None = None
     frequency: str | None = None

class TaskCreate(SQLModel):
     title: str 
     priority: str
     done: bool = False
     due_date: str | None = None
     frequency: str | None = None

class TaskUpdate(SQLModel):
     title: str | None = None
     priority: str | None = None
     done: bool | None = None 
     due_date: str | None = None
     frequency: str | None = None

class User(SQLModel, table=True):
     id: int | None = Field(default=None, primary_key=True)
     username: str = Field(unique=True)
     hashed_password: str
class UserCreate(SQLModel):
     username: str
     password: str
     
engine = create_engine("sqlite:///tracker.db")
SQLModel.metadata.create_all(engine)

app = FastAPI() #fastapi client
ph = PasswordHasher()

@app.get("/tasks") # get endpoint used to list all tasks
def list_tasks():
      with Session(engine) as session:
           return session.exec(select(Task)).all()

@app.post("/tasks")
def create_task(task_in: TaskCreate):
     task = Task(**task_in.model_dump())
     with Session(engine) as session:
          session.add(task)
          session.commit()
          session.refresh(task)
          return task

@app.post("/register")
def register(user_in: UserCreate):
     hashed = ph.hash(user_in.password)
     user = User(username=user_in.username, hashed_password=hashed)
     with Session(engine) as session:
          session.add(user)
          session.commit()
          session.refresh(user)
          return {"message": f"User {user.username} created"}

@app.delete("/tasks/{title}")
def delete_task(title: str):
     with Session(engine) as session:
          statement = select(Task).where(Task.title == title)
          task = session.exec(statement).first()
          if not task:
               raise HTTPException(status_code=404, detail="Task not found")
          session.delete(task)
          session.commit()
          return {"message": f"Deleted {title}"}

@app.get("/tasks/filter")
def filter_tasks(priority: str):
     with Session(engine) as session:
          statement = select(Task).where(Task.priority == priority)
          return session.exec(statement).all()

@app.put("/tasks/{title}")
def update_task(title: str, updated:TaskUpdate):
     with Session(engine) as session:
          statement = select(Task).where(Task.title == title)
          task = session.exec(statement).first()
          if not task:
               raise HTTPException(status_code=404, detail="Task not found")

          if updated.title is not None:
               task.title = updated.title
          if updated.priority is not None:
               task.priority = updated.priority
          if updated.done is not None:
               task.done = updated.done
          if updated.due_date is not None:
               task.due_date = updated.due_date
          if updated.frequency is not None:
               task.frequency = updated.frequency

          session.add(task)
          session.commit()
          return task