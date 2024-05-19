from fastapi import FastAPI, HTTPException, Form, Request, Cookie, Response, Depends, WebSocket
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from itsdangerous import URLSafeSerializer
from pydantic import BaseModel
from typing import List
import psycopg2
from psycopg2 import sql
import os
from datetime import datetime

app = FastAPI()
templates = Jinja2Templates(directory='./public')

# 데이터베이스 연결 정보
USER_DB_CONFIG = {
    "host": "dpg-cp4pc6q1hbls73f4lf80-a.oregon-postgres.render.com",
    "database": "db_fahq",
    "user": "hwanghj09",
    "password": "ru0U1ZfFZvtR5ppaKbr85ZqjDZL5tcmo"
}

SECRET_KEY = "JEOFIGHTING"
serializer = URLSafeSerializer(SECRET_KEY)
manager = ["hwanghj09", "dreami"]

def is_manager(username: str, managers: List[str]) -> bool:
    return username in managers

def get_db_connection(db_config):
    return psycopg2.connect(**db_config)

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
async def community(request: Request):
    conn = get_db_connection(USER_DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM board")
    posts = cursor.fetchall()
    cursor.close()
    conn.close()
    return templates.TemplateResponse("community.html", {"request": request, "posts": posts})

@app.get("/create_post")
async def create_post(request: Request, username: str = Cookie(None)):
    if username is None:
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
def model(request: Request):
    return templates.TemplateResponse('3d.html', context={'request': request})

@app.get("/admin/inquiries")
async def get_inquiries(request: Request, username: str = Cookie(None)):
    username = serializer.loads(username)
    if not is_manager(username, manager):
        raise HTTPException(status_code=302, detail="Unauthorized", headers={"Location": "/index"})
    conn = get_db_connection(USER_DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inquiry")
    inquiries = cursor.fetchall()
    cursor.close()
    conn.close()
    print(inquiries)
    return templates.TemplateResponse("admin_inquiries.html", {"request": request, "inquiries": inquiries})

@app.get("/admin/users")
async def get_users(request: Request, username: str = Cookie(None)):
    username = serializer.loads(username)
    if not is_manager(username, manager):
        raise HTTPException(status_code=302, detail="Unauthorized", headers={"Location": "/index"})
    conn = get_db_connection(USER_DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users_table")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return templates.TemplateResponse("admin_users.html", {"request": request, "Users": users})

@app.get("/admin/users/reset_password/{user_id}")
async def reset_password(user_id: int, username: str = Cookie(None)):
    username = serializer.loads(username)
    if not is_manager(username, manager):
        raise HTTPException(status_code=302, detail="Unauthorized", headers={"Location": "/index"})
    conn = get_db_connection(USER_DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("UPDATE users_table SET password = %s WHERE id = %s", ("1234", user_id))
    conn.commit()
    cursor.close()
    conn.close()
    return RedirectResponse(url="/admin/users", status_code=303)

@app.get("/check_login")
async def check_login(username: str = Cookie(None)):
    if username:
        return {"login": True}, FileResponse('public/index.html')
    else:
        return {"login": False}, FileResponse('public/index.html')

@app.get("/logout")
async def logout(request: Request):
    response = templates.TemplateResponse("index.html", {"request": request})
    response.delete_cookie(key="username")
    return response

@app.get("/view_board/{post_id}")
async def view_board(post_id: int, request: Request, username: str = Cookie(None)):
    username = serializer.loads(username)
    conn = get_db_connection(USER_DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM board WHERE id = %s", (post_id,))
    post = cursor.fetchone()
    cursor.close()
    conn.close()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    manager_check = is_manager(username, manager)
    return templates.TemplateResponse("view_board.html", {"request": request, "post": post, "username": username, "manager_check": manager_check})

@app.get("/modify_post/{post_id}")
async def modify_post(post_id: int, request: Request, username: str = Cookie(None)):
    username = serializer.loads(username)
    conn = get_db_connection(USER_DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM board WHERE id = %s", (post_id,))
    post = cursor.fetchone()
    cursor.close()
    conn.close()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return templates.TemplateResponse("modify_post.html", {"request": request, "post": post})

@app.get("/paint_board")
def paintboard(request: Request):
    return templates.TemplateResponse("paint_board.html", {"request": request})

@app.get("/zizon-shopping")
def zizon_shopping(request: Request):
    return templates.TemplateResponse("쇼핑/index.html", {"request": request})

@app.get("/shop")
async def shop(request: Request):
    conn = get_db_connection(USER_DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return templates.TemplateResponse("쇼핑/shop.html", {"request": request, "products": products})

@app.get("/product/{product_id}")
async def product_detail(product_id: int, request: Request):
    conn = get_db_connection(USER_DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    cursor.close()
    conn.close()
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
def spot_signup(request: Request):
    return templates.TemplateResponse("spot/Signup.html", {"request": request})

@app.get("/spot/login")
def spot_login(request: Request):
    return templates.TemplateResponse("spot/Login.html", {"request": request})

@app.get("/spot/AIQ.")
def spot_aiq(request: Request):
    return templates.TemplateResponse("spot/AIQ..html", {"request": request})

@app.get("/spot/about")
def spot_about(request: Request):
    return templates.TemplateResponse("spot/aboutSpot+.html", {"request": request})

@app.post("/post_register")
def process_register(username: str = Form(...), password: str = Form(...)):
    conn = get_db_connection(USER_DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users_table WHERE name = %s", (username,))

    existing_user = cursor.fetchone()
    if existing_user:
        cursor.close()
        conn.close()
        return FileResponse('public/register.html')

    cursor.execute("INSERT INTO users_table (name, password) VALUES (%s, %s)", (username, password))
    conn.commit()
    cursor.close()
    conn.close()

    response = FileResponse("public/index.html")
    encrypted_username = serializer.dumps(username)
    response.set_cookie(key="username", value=encrypted_username, max_age=30*24*60*60)
    return response

@app.post("/post_login")
def process_login(request: Request, username: str = Form(...), password: str = Form(...)):
    conn = get_db_connection(USER_DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users_table WHERE name = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if not user:
        return FileResponse('public/login.html')

    response = FileResponse('public/index.html')
    encrypted_username = serializer.dumps(username)
    response.set_cookie(key="username", value=encrypted_username, max_age=30*24*60*60)
    return response

@app.post("/spot/post_register")
def spot_process_register(username: str = Form(...), password: str = Form(...)):
    conn = get_db_connection(USER_DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users_table WHERE name = %s", (username,))
    existing_user = cursor.fetchone()
    if existing_user:
        cursor.close()
        conn.close()
        return FileResponse('public/spot/Login.html')

    cursor.execute("INSERT INTO users_table (name, password) VALUES (%s, %s)", (username, password))
    conn.commit()
    cursor.close()
    conn.close()

    response = FileResponse("public/spot/home.html")
    encrypted_username = serializer.dumps(username)
    response.set_cookie(key="username", value=encrypted_username, max_age=30*24*60*60)
    return response

@app.post("/spot/post_login")
def spot_process_login(request: Request, username: str = Form(...), password: str = Form(...)):
    conn = get_db_connection(USER_DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users_table WHERE name = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if not user:
        return FileResponse('public/spot/Login.html')

    response = FileResponse('public/spot/home.html')
    encrypted_username = serializer.dumps(username)
    response.set_cookie(key="username", value=encrypted_username, max_age=30*24*60*60)
    return response

@app.post("/submit_contact_form")
async def submit_contact_form(request: Request):
    form_data = await request.form()
    name = form_data.get("name")
    title = form_data.get("title")
    message = form_data.get("message")
    conn = get_db_connection(USER_DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO inquiry (username, title, content) VALUES (%s, %s, %s)", (name, title, message))
    conn.commit()
    cursor.close()
    conn.close()

    return templates.TemplateResponse('inquiry.html', context={"request": request})

@app.post("/create_post")
async def create_post(request: Request, title: str = Form(...), content: str = Form(...), username: str = Cookie(None)):
    username = serializer.loads(username)
    created_at = datetime.now()  # 현재 시간을 가져옴
    conn = get_db_connection(USER_DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO board (title, author, content, created_at) VALUES (%s, %s, %s, %s)", (title, username, content, created_at))
    conn.commit()
    cursor.close()
    conn.close()
    return RedirectResponse(url="/community", status_code=303)

@app.post("/modify_post/{post_id}")
async def modify_post(post_id: int, request: Request, title: str = Form(...), content: str = Form(...), username: str = Cookie(None)):
    username = serializer.loads(username)
    conn = get_db_connection(USER_DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM board WHERE id = %s", (post_id,))
    post = cursor.fetchone()
    if not post:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Post not found")

    cursor.execute("UPDATE board SET title = %s, content = %s WHERE id = %s", (title, content, post_id))
    conn.commit()
    cursor.close()
    conn.close()
    return RedirectResponse(url=f"/view_board/{post_id}", status_code=303)

@app.delete("/delete_post/{post_id}")
async def delete_post(post_id: int, request: Request, username: str = Cookie(None)):
    username = serializer.loads(username)
    conn = get_db_connection(USER_DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM board WHERE id = %s", (post_id,))
    post = cursor.fetchone()
    if not post:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Post not found")

    if post[2] != username and not is_manager(username, manager):  # assuming author is the third field in the table
        cursor.close()
        conn.close()
        raise HTTPException(status_code=403, detail="You are not authorized to delete this post")

    cursor.execute("DELETE FROM board WHERE id = %s", (post_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return RedirectResponse(url="/community", status_code=303)