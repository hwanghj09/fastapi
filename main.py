from fastapi import FastAPI, HTTPException, Form, Request, Cookie,Response
from fastapi.responses import FileResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import engineconn
from model import User
from itsdangerous import URLSafeSerializer

app = FastAPI()
templates = Jinja2Templates(directory='./public')
engine = engineconn()
session = engine.sessionmaker()
SECRET_KEY = "JEOFIGHTING"
serializer = URLSafeSerializer(SECRET_KEY)

@app.get("/")
def main():
    return FileResponse('public/index.html')

@app.get("/index")
def main():
    return FileResponse('public/index.html')

@app.get("/register")
def register(request: Request):
    return templates.TemplateResponse('register.html', context={'request': request})

@app.get("/login")
def login(request: Request):
    return templates.TemplateResponse('login.html', context={'request': request})

@app.get("/community")
def community(request: Request):
    return templates.TemplateResponse('community.html', context={'request': request})

@app.post("/post_register")
def process_register(username: str = Form(...), password: str = Form(...)):
    existing_user = session.query(User).filter_by(name=username).first()
    if existing_user:
        return FileResponse('public/register.html')
    new_user = User(name=username, password=password)
    session.add(new_user)
    session.commit()
    
    response = FileResponse("public/index.html")  # 회원가입 성공 시 /index로 이동
    
    # 유저 정보를 쿠키에 저장 (예시로 만료 날짜는 30일 후로 설정)
    encrypted_username = serializer.dumps(username)
    response.set_cookie(key="username", value=encrypted_username, max_age=30*24*60*60)  # 30일의 초로 설정
    
    return response

@app.post("/post_login")
def process_login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = session.query(User).filter_by(name=username, password=password).first()
    if not user:
        return FileResponse('public/index.html')  # 로그인 실패 시 로그인 페이지로 리다이렉트
    
    response = FileResponse('public/index.html')  # 로그인 성공 시 /index.html 파일을 반환
    
    # 유저 정보를 쿠키에 저장 (예시로 만료 날짜는 30일 후로 설정)
    encrypted_username = serializer.dumps(username)
    response.set_cookie(key="username", value=encrypted_username, max_age=30*24*60*60)  # 30일의 초로 설정
    
    return response
        