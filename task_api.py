import os
from dotenv import load_dotenv
from jose import jwt, JWTError
from argon2 import PasswordHasher
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from argon2.exceptions import VerifyMismatchError
from datetime import datetime, timezone, timedelta
from sqlmodel import SQLModel, Field, create_engine, Session, select

SECRET_KEY = os.getenv("SECRET_KEY") # secret key, exposed for now just for practice
ALGORITHM = "HS256"          # hashing algorithm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") # finding the token request

def create_access_token(username: str): # creating access token
     expire = datetime.now(timezone.utc) + timedelta(minutes=30)
     data = {"sub": username, "exp": expire}
     token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
     return token

def get_current_user(token: str = Depends(oauth2_scheme)): # decoding the payload & checking if token  
     try:                                                  # signature matches
          payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
          username = payload.get("sub")
          if username is None:
               raise HTTPException(status_code=401, detail="Invalid token")

          with Session(engine) as session:
               statement = select(User).where(User.username == username)
               user = session.exec(statement).first()

               if not user:
                    raise HTTPException(status_code=401, detail="User Not Found")
               return user.id           # returned id because unlike usernames, id can not be changed
     except JWTError:
          raise HTTPException(status_code=401, detail="Invalid token")
class Task(SQLModel, table=True): # creating a table with task information
     __tablename__ = "tasks"
     id: int | None = Field(default=None, primary_key=True)
     title: str 
     priority: str
     done: bool = False
     due_date: str | None = None
     frequency: str | None = None
     owner: int
class TaskCreate(SQLModel):   # task creation
     title: str 
     priority: str
     done: bool = False
     due_date: str | None = None
     frequency: str | None = None
class TaskUpdate(SQLModel):   # updating an existing task
     title: str | None = None
     priority: str | None = None
     done: bool | None = None 
     due_date: str | None = None
     frequency: str | None = None
class User(SQLModel, table=True): # username and hashed password table
     id: int | None = Field(default=None, primary_key=True)
     username: str = Field(unique=True)
     hashed_password: str
class UserCreate(SQLModel):    # collecting user login info
     username: str
     password: str
     
engine = create_engine("sqlite:///tracker.db")
SQLModel.metadata.create_all(engine)

app = FastAPI()                #fastapi client
ph = PasswordHasher()

@app.get("/tasks")             # get endpoint used to list all tasks
def list_tasks(user_id: int = Depends(get_current_user)):
      with Session(engine) as session:
           statement = select(Task).where(Task.owner == user_id)
           return session.exec(statement).all()

@app.post("/tasks")
def create_task(task_in: TaskCreate, user_id: int = Depends(get_current_user)):
     task = Task(**task_in.model_dump(), owner=user_id)
     with Session(engine) as session:
          session.add(task)
          session.commit()
          session.refresh(task)
          return task

@app.post("/register")        # post endpoint to register a new user and password
def register(user_in: UserCreate):
     hashed = ph.hash(user_in.password)
     user = User(username=user_in.username, hashed_password=hashed)
     with Session(engine) as session:
          session.add(user)
          session.commit()
          session.refresh(user)
          return {"message": f"User {user.username} created"}

@app.post("/login")           # authenticating and login in the user
def login(form_data: OAuth2PasswordRequestForm = Depends()):
     with Session(engine) as session:
          statement = select(User).where(User.username == form_data.username)
          user = session.exec(statement).first()
          if not user:
               raise HTTPException(status_code=401, detail="Invalid username or password")
          try:
               ph.verify(user.hashed_password, form_data.password)
          except VerifyMismatchError:
               raise HTTPException(status_code=401, detail="Invalid username or password")

          token = create_access_token(user.username)
          return {"access_token": token, "token_type": "bearer"}

@app.delete("/tasks/{title}") # deleting a task endpont
def delete_task(title: str, user_id: int = Depends(get_current_user)):
     with Session(engine) as session:
          statement = select(Task).where(Task.title == title).where(Task.owner == user_id)
          task = session.exec(statement).first()
          if not task:
               raise HTTPException(status_code=404, detail="Task not found")
          session.delete(task)
          session.commit()
          return {"message": f"Deleted {title}"}

@app.get("/tasks/filter")     # filtering tasks endpoint
def filter_tasks(priority: str, user_id: int = Depends(get_current_user)):
     with Session(engine) as session:
          statement = select(Task).where(Task.priority == priority).where(Task.owner == user_id)
          return session.exec(statement).all()

@app.put("/tasks/{title}")    # updating tasks endpoint
def update_task(title: str, updated:TaskUpdate, user_id: int = Depends(get_current_user)):
     with Session(engine) as session:
          statement = select(Task).where(Task.title == title).where(Task.owner == user_id)
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
