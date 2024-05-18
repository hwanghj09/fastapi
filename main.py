from fastapi import FastAPI, HTTPException, Form, Request, Cookie, Response, Depends,WebSocket
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import session
from database import Usersengineconn
from database import Shoppingengineconn
from model import User, Inquiry, Board, Product
from itsdangerous import URLSafeSerializer
from pydantic import BaseModel
from typing import List


app = FastAPI()
templates = Jinja2Templates(directory='./public')

Userengine = Usersengineconn()
Usersession = Userengine.sessionmaker()
Shoppingengine = Shoppingengineconn()
Shoppingsession = Shoppingengine.sessionmaker()

SECRET_KEY = "JEOFIGHTING"
serializer = URLSafeSerializer(SECRET_KEY)
manager = ["hwanghj09", "dreami"]
websocket_list: List[WebSocket] = []
message_history: List[str] = []

def is_manager(username: str, managers: List[str]) -> bool:
    return username in managers

@app.get("/")
def main(request: Request):
    return templates.TemplateResponse('index.html', context={'request': request})

@app.get("/index")
def main(request: Request):
    return templates.TemplateResponse('index.html', context={'request': request})

@app.get("/register")
def register(request: Request):
    return templates.TemplateResponse('register.html', context={'request': request})

@app.get("/login")
def login(request: Request):
    return templates.TemplateResponse('login.html', context={'request': request})

@app.get("/community")
async def community(request: Request, db: Usersession = Depends(Usersengineconn().sessionmaker)):
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

@app.get("/3d")
def model(request:Request):
    return templates.TemplateResponse('3d.html', context={'request': request})
@app.get("/admin/inquiries")
async def get_inquiries(request: Request, db: Usersession = Depends(Usersengineconn().sessionmaker) , username: str = Cookie(None)):
    username = serializer.loads(username)
    if not is_manager(username, manager):
        raise HTTPException(status_code=302, detail="Unauthorized", headers={"Location": "/index"})
    inquiries = db.query(Inquiry).all()  # 모든 문의 내역을 가져옵니다.
    return templates.TemplateResponse("admin_inquiries.html", {"request": request, "inquiries": inquiries})

@app.get("/admin/users")
async def get_inquiries(request: Request, db: Usersession = Depends(Usersengineconn().sessionmaker) , username: str = Cookie(None)):
    username = serializer.loads(username)
    if not is_manager(username, manager):
        raise HTTPException(status_code=302, detail="Unauthorized", headers={"Location": "/index"})
    Users = db.query(User).all()  # 모든 문의 내역을 가져옵니다.
    return templates.TemplateResponse("admin_users.html", {"request": request, "Users": Users})

@app.get("/admin/users/reset_password/{user_id}")
async def reset_password(user_id: int, db: Usersession = Depends(Usersengineconn().sessionmaker), username: str = Cookie(None)):
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
        return {"login": True}, FileResponse('public/index.html')
    else:
        return {"login": False}, FileResponse('public/index.html')
    
@app.get("/logout")
async def logout(request: Request):
    response = templates.TemplateResponse("index.html", {"request":request})
    response.delete_cookie(key="username")
    return response

@app.get("/view_board/{post_id}")
async def view_board(post_id: int, db: Usersession = Depends(Usersengineconn().sessionmaker), request: Request = None, username: str = Cookie(None), manager_check: bool = False):
    username=serializer.loads(username)
    post = db.query(Board).filter(Board.id == post_id).first()
    manager_check=False
    if is_manager(username, manager)==True:
        manager_check=True
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return templates.TemplateResponse("view_board.html", {"request": request, "post": post, "username": username, "manager_check": manager_check})

@app.get("/modify_post/{post_id}")
async def modify_post(post_id: int,db: Usersession = Depends(Usersengineconn().sessionmaker), request: Request = None, username: str = Cookie(None)):
    post = db.query(Board).filter(Board.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if(username==post.author):
        return templates.TemplateResponse("view_board.html", {"request": request})
    return templates.TemplateResponse("modify_post.html", {"request": request, "post": post})

@app.get("/paint_board")
def paintboard(request: Request):
    return templates.TemplateResponse("paint_board.html", {"request": request})

@app.get("/zizon-shopping")
def paintboard(request: Request):
    return templates.TemplateResponse("쇼핑/index.html", {"request": request})
@app.get("/shop")
async def shop(request: Request, db: Shoppingsession = Depends(Shoppingengineconn().sessionmaker)):
    products = db.query(Product).all()
    return templates.TemplateResponse("쇼핑/shop.html", {"request": request, "products": products})
@app.get("/product/{product_id}")
async def product_detail(product_id: int, request: Request, db: Shoppingsession = Depends(Shoppingengineconn().sessionmaker)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return templates.TemplateResponse("쇼핑/product.html", {"request": request, "product": product})
@app.get("/guide")
def guide(request: Request):
    return templates.TemplateResponse("쇼핑/guide.html", {"request": request})

@app.get("/spot")
def spot(request: Request):
    return templates.TemplateResponse("spot/home.html", {"request": request})
@app.get("/spot/signup")
def spot(request: Request):
    return templates.TemplateResponse("spot/Signup.html", {"request": request})
@app.get("/spot/login")
def spot(request: Request):
    return templates.TemplateResponse("spot/Login.html", {"request": request})
@app.get("/spot/AIQ.")
def spot(request: Request):
    return templates.TemplateResponse("spot/AIQ..html", {"request": request})
@app.get("/spot/about")
def spot(request: Request):
    return templates.TemplateResponse("spot/aboutSpot+.html", {"request": request})
#------------------------------------------------------------------------------------

@app.post("/post_register")
def process_register(username: str = Form(...), password: str = Form(...)):
    existing_user = Usersession.query(User).filter_by(name=username).first()
    if existing_user:
        return FileResponse('public/register.html')
    new_user = User(name=username, password=password)
    Usersession.add(new_user)
    Usersession.commit()
    
    response = FileResponse("public/index.html")  # 회원가입 성공 시 /index로 이동
    
    # 유저 정보를 쿠키에 저장 (예시로 만료 날짜는 30일 후로 설정)
    encrypted_username = serializer.dumps(username)
    response.set_cookie(key="username", value=encrypted_username, max_age=30*24*60*60)  # 30일의 초로 설정
    
    return response

@app.post("/post_login")
def process_login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = Usersession.query(User).filter_by(name=username, password=password).first()
    if not user:
        return FileResponse('public/login.html')  # 로그인 실패 시 로그인 페이지로 리다이렉트
    
    response = FileResponse('public/index.html')  # 로그인 성공 시 /index.html 파일을 반환
    
    # 유저 정보를 쿠키에 저장 (예시로 만료 날짜는 30일 후로 설정)
    encrypted_username = serializer.dumps(username)
    response.set_cookie(key="username", value=encrypted_username, max_age=30*24*60*60)  # 30일의 초로 설정

    return response

@app.post("/spot/post_register")
def process_register(username: str = Form(...), password: str = Form(...)):
    existing_user = Usersession.query(User).filter_by(name=username).first()
    if existing_user:
        return FileResponse('public/spot/Login.html')
    new_user = User(name=username, password=password)
    Usersession.add(new_user)
    Usersession.commit()
    
    response = FileResponse("public/spot/home.html")  # 회원가입 성공 시 /index로 이동
    
    # 유저 정보를 쿠키에 저장 (예시로 만료 날짜는 30일 후로 설정)
    encrypted_username = serializer.dumps(username)
    response.set_cookie(key="username", value=encrypted_username, max_age=30*24*60*60)  # 30일의 초로 설정
    
    return response

@app.post("/spot/post_login")
def process_login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = Usersession.query(User).filter_by(name=username, password=password).first()
    if not user:
        return FileResponse('public/spot/Login.html')  # 로그인 실패 시 로그인 페이지로 리다이렉트
    
    response = FileResponse('public/spot/home.html')  # 로그인 성공 시 /index.html 파일을 반환
    
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
    db = Usersengineconn().sessionmaker()
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
    Usersession.add(new_post)
    Usersession.commit()
    return RedirectResponse(url="/community", status_code=303)


@app.post("/modify_post/{post_id}")
async def modify_post(post_id: int, request: Request, title: str = Form(...), content: str = Form(...), username: str = Cookie(None), db: Usersession = Depends(Usersengineconn().sessionmaker)):
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


#-------------------------------------------------------------------------------


@app.delete("/delete_post/{post_id}")
async def delete_post(post_id: int, request: Request, username: str = Cookie(None), db: Usersession = Depends(Usersengineconn().sessionmaker)):
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