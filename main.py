from fastapi import FastAPI, HTTPException, Form, Request, Cookie, Response, Depends
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import engineconn
from model import User, Inquiry, Board
from itsdangerous import URLSafeSerializer
from pydantic import BaseModel
from typing import List

app = FastAPI()
templates = Jinja2Templates(directory='./public')
engine = engineconn()
session = engine.sessionmaker()
SECRET_KEY = "JEOFIGHTING"
serializer = URLSafeSerializer(SECRET_KEY)
manager = ["hwanghj09"]

def is_manager(username: str, managers: List[str]) -> bool:
    return username in managers

@app.get("/")
def main(request: Request, username: str = Cookie(None)):
    username = serializer.loads(username)
    manager_check = is_manager(username, manager)  # 여기서 전역 변수 manager를 전달해야 합니다.
    return templates.TemplateResponse('index.html', context={'request': request, "username":username, "manager":manager_check})

@app.get("/index")
def main(request: Request, username: str = Cookie(None)):
    username = serializer.loads(username)
    manager_check = is_manager(username, manager)  # 여기서 전역 변수 manager를 전달해야 합니다.
    return templates.TemplateResponse('index.html', context={'request': request, "username":username, "manager":manager_check})

@app.get("/register")
def register(request: Request):
    return templates.TemplateResponse('register.html', context={'request': request})

@app.get("/login")
def login(request: Request):
    return templates.TemplateResponse('login.html', context={'request': request})

@app.get("/community")
async def community(request: Request, db: Session = Depends(engineconn().sessionmaker)):
    posts = db.query(Board).all()
    return templates.TemplateResponse("community.html", {"request": request, "posts": posts})

@app.get("/create_post")
async def create_post(request: Request, username: str = Cookie(None)):
    if(username == None):
        return templates.TemplateResponse("login.html", {"request": request})
    return templates.TemplateResponse("create_post.html", {"request": request})


@app.get("/inquiry")
def inquiry(request: Request):
    return templates.TemplateResponse('inquiry.html', context={'request': request})

@app.get("/admin")
def admin(request: Request, username: str = Cookie(None)):
    username = serializer.loads(username)
    if not is_manager(username, manager):
        raise HTTPException(status_code=302, detail="Unauthorized", headers={"Location": "/index"})
    return templates.TemplateResponse('admin.html', context={'request': request})

@app.get("/admin/inquiries")
async def get_inquiries(request: Request, db: Session = Depends(engineconn().sessionmaker) , username: str = Cookie(None)):
    username = serializer.loads(username)
    if not is_manager(username, manager):
        raise HTTPException(status_code=302, detail="Unauthorized", headers={"Location": "/index"})
    inquiries = db.query(Inquiry).all()  # 모든 문의 내역을 가져옵니다.
    return templates.TemplateResponse("admin_inquiries.html", {"request": request, "inquiries": inquiries})

@app.get("/admin/users")
async def get_inquiries(request: Request, db: Session = Depends(engineconn().sessionmaker) , username: str = Cookie(None)):
    username = serializer.loads(username)
    if not is_manager(username, manager):
        raise HTTPException(status_code=302, detail="Unauthorized", headers={"Location": "/index"})
    Users = db.query(User).all()  # 모든 문의 내역을 가져옵니다.
    return templates.TemplateResponse("admin_users.html", {"request": request, "Users": Users})

@app.get("/admin/users/reset_password/{user_id}")
async def reset_password(user_id: int, db: Session = Depends(engineconn().sessionmaker), username: str = Cookie(None)):
    username = serializer.loads(username)
    if not is_manager(username, manager):
        raise HTTPException(status_code=302, detail="Unauthorized", headers={"Location": "/index"})
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 비밀번호를 변경하여 저장
    user.password = "1234"
    db.commit()
    
    return RedirectResponse(url="/admin/users", status_code=303)


@app.get("/check_login")
async def check_login(username: str = Cookie(None)):
    if username:
        return {"login" : True}, FileResponse('public/index.html')
    else:
        return {"login" : False}, FileResponse('public/index.html')
    
@app.get("/logout")
async def logout(request: Request):
    response = templates.TemplateResponse("index.html", {"request":request})
    response.delete_cookie(key="username")
    return response

@app.get("/view_board/{post_id}")
async def view_board(post_id: int, db: Session = Depends(engineconn().sessionmaker), request: Request = None, username: str = Cookie(None)):
    username=serializer.loads(username)
    manager_check = is_manager(username, manager)
    post = db.query(Board).filter(Board.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return templates.TemplateResponse("view_board.html", {"request": request, "post": post, "username": username, "manager_check":manager_check})

@app.get("/modify_post/{post_id}")
async def modify_post(post_id: int,db: Session = Depends(engineconn().sessionmaker), request: Request = None, username: str = Cookie(None)):
    post = db.query(Board).filter(Board.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if(username==post.author):
        return templates.TemplateResponse("view_board.html", {"request": request})
    return templates.TemplateResponse("modify_post.html", {"request": request, "post": post})

#------------------------------------------------------------------------------------

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
        return FileResponse('public/login.html')  # 로그인 실패 시 로그인 페이지로 리다이렉트
    
    response = FileResponse('public/index.html')  # 로그인 성공 시 /index.html 파일을 반환
    
    # 유저 정보를 쿠키에 저장 (예시로 만료 날짜는 30일 후로 설정)
    encrypted_username = serializer.dumps(username)
    response.set_cookie(key="username", value=encrypted_username, max_age=30*24*60*60)  # 30일의 초로 설정

    return response


@app.post("/submit_contact_form")
async def submit_contact_form(request: Request):
    form_data = await request.form()
    name = form_data.get("name")
    title = form_data.get("title")
    message = form_data.get("message")

    # 데이터베이스에 저장
    db = engineconn().sessionmaker()
    new_inquiry = Inquiry(username=name, title=title, content=message)
    db.add(new_inquiry)
    db.commit()
    db.close()

    return templates.TemplateResponse('inquiry.html', context={"request":request})


# 게시글 작성 처리
@app.post("/create_post")
async def create_post(request: Request, title: str = Form(...),content: str = Form(...), username: str = Cookie(None)):
    username=serializer.loads(username)
    new_post = Board(title=title, author=username, content=content)
    session.add(new_post)
    session.commit()
    return RedirectResponse(url="/community", status_code=303)


@app.post("/modify_post/{post_id}")
async def modify_post(post_id: int, request: Request, title: str = Form(...), content: str = Form(...), username: str = Cookie(None), db: Session = Depends(engineconn().sessionmaker)):
    username = serializer.loads(username)
    post = db.query(Board).filter(Board.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.author != username:
        raise HTTPException(status_code=403, detail="You are not authorized to modify this post")

    # Update the post with the new title and content
    post.title = title
    post.content = content
    db.commit()  # Save the changes to the database

    return RedirectResponse(url=f"/view_board/{post_id}", status_code=303)

@app.delete("/delete_post/{post_id}")
async def delete_post(post_id: int, request: Request, username: str = Cookie(None), db: Session = Depends(engineconn().sessionmaker)):
    username = serializer.loads(username)
    post = db.query(Board).filter(Board.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if(post.author != username and is_manager(username, manager)==False):
        raise HTTPException(status_code=403, detail="You are not authorized to delete this post")

    # Delete the post from the database
    db.delete(post)
    db.commit()

    return RedirectResponse(url="/community", status_code=303)



