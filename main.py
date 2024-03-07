from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.templating import Jinja2Templates
from database import engineconn
from model import User

app = FastAPI()
templates = Jinja2Templates(directory='/public')
engine = engineconn()
session = engine.sessionmaker()

@app.get("/")
def main(request: Request):
    return templates.TemplateResponse('index.html', context={'request': request})

@app.get("/register")
def register(request: Request):
    return templates.TemplateResponse('register.html', context={'request': request})

@app.get("/check_grade")
def check_grade(request: Request):
    return templates.TemplateResponse('check_grade.html', context={'request': request})

@app.get("/login")
def login(request: Request):
    return templates.TemplateResponse('login.html', context={'request': request})

@app.post("/post_register")
def process_register(username: str = Form(...), password: str = Form(...)):
    existing_user = session.query(User).filter_by(name=username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    new_user = User(name=username, password=password)
    session.add(new_user)
    session.commit()
    all_users = session.query(User).all()

    return {"message": f"User {username} registered successfully", "all_users": all_users}

@app.post("/post_login")
def process_login(username: str = Form(...), password: str = Form(...)):
    user = session.query(User).filter_by(name=username, password=password).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"message": f"User {username} logged in successfully"}