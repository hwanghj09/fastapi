from fastapi import FastAPI, HTTPException, Form, Request
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import engineconn
from model import User

app = FastAPI()
templates = Jinja2Templates(directory='./public')
engine = engineconn()
session = engine.sessionmaker()

@app.get("/")
def main():
    return FileResponse('public/index.html')

@app.get("/register")
def register(request: Request):
    return templates.TemplateResponse('register.html', context={'request': request})

@app.get("/check_grade")
def check_grade(request: Request):
    return templates.TemplateResponse('check_grade.html', context={'request': request})

@app.get("/login")
def login(request: Request):
    return templates.TemplateResponse('login.html', context={'request': request})

@app.get("/community")
def community(request: Request):
    return templates.TemplateResponse('community.html', context={'request':request})

@app.post("/post_register")
def process_register(username: str = Form(...), password: str = Form(...)):
    existing_user = session.query(User).filter_by(name=username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    new_user = User(name=username, password=password)
    session.add(new_user)
    session.commit()
    response = RedirectResponse(url="/login")
    return response

@app.post("/post_login")
def process_login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = session.query(User).filter_by(name=username, password=password).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    response = RedirectResponse(url="/")
    return response

