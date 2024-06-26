from fastapi import FastAPI, HTTPException, Form, Request, Cookie, Response
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from itsdangerous import URLSafeSerializer
from typing import List
import psycopg2
from datetime import datetime
import random
import math
import sympy as sp

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

@app.get("/study/{subject}/{unit}")
def study(request: Request, subject: str, unit: str):
    return templates.TemplateResponse(subject+'.html', context={'request': request, 'unit':unit})

@app.get("/game")
def login(request: Request):
    return templates.TemplateResponse('game.html', context={'request': request})
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

@app.post("/study/math/암산게임")
def mathgame(request: Request):
    num1 = random.randint(100, 999)
    num2 = random.randint(100, 999)
    operations = ['+', '-', '*', '/']
    operation = random.choice(operations)
    problem = f"{num1} {operation} {num2}"
    if operation == '+':
        answer = num1 + num2
    elif operation == '-':
        answer = num1 - num2
    elif operation == '*':
        answer = num1 * num2
    else:
        answer = num1 // num2

    return {"problem": problem, "answer": answer}

def generate_quadratic_equation():
    while True:
        a = random.choice([random.randint(-10, -1), random.randint(1, 10)])  # -10에서 -1 또는 1에서 10 사이의 랜덤한 값
        b = random.choice([random.randint(-10, -1), random.randint(1, 10)])
        c = random.choice([random.randint(-10, -1), random.randint(1, 10)])
        
        discriminant = b**2 - 4*a*c
        if discriminant >= 0:  # 근이 정수인 경우에만 종료
            root1 = (-b + math.sqrt(discriminant)) / (2*a)
            root2 = (-b - math.sqrt(discriminant)) / (2*a)
            if root1.is_integer() and root2.is_integer():
                return a, b, c

def quadratic_roots(a, b, c):
    discriminant = b**2 - 4*a*c
    if discriminant > 0:
        root1 = (-b + math.sqrt(discriminant)) / (2*a)
        root2 = (-b - math.sqrt(discriminant)) / (2*a)
        return root1, root2
    elif discriminant == 0:
        root = -b / (2*a)
        return root,
    else:
        return "근은 실수입니다."

@app.post("/study/math/이차방정식")
async def mathgame(request: Request):
    # 랜덤한 이차방정식 생성
    a, b, c = generate_quadratic_equation()

    equation = f"{a}x² +{b}x +{c} = 0"

    # 근 계산
    roots = quadratic_roots(a, b, c)
    
    return {"problem": equation, "answer": roots}

@app.post("/study/math/이차방정식활용")
async def mathgame(request: Request):
    problem_data = generate_quadratic_problem()
    return {"problem": problem_data["problem"], "answer": problem_data["answer"]}
def generate_quadratic_problem():
    problems = [
        generate_area_problem,
        generate_consecutive_odd_problem,
        generate_road_width_problem
    ]
    # 랜덤하게 문제 유형을 선택합니다.
    problem_func = random.choice(problems)
    return problem_func()

def generate_area_problem():
    # 랜덤한 가로 세로 선택 (정수로 선택)
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    c = a * b
    
    equation = f"x^2 - ({a + b})x + {c} = 0"
    x = sp.symbols('x')
    area_equation = x**2 - (a + b)*x + c
    solutions = sp.solve(area_equation, x)
    # 실수 해 중에서 정수로 된 해를 선택하고 허수 해는 제외합니다.
    solutions = [int(sol.evalf()) for sol in solutions if sol.is_real and sol > 0 and sol.is_integer]
    
    problem = f"가로 길이가 {a} cm, 세로 길이가 {b} cm인 직사각형의 넓이는 {c} cm^2입니다. 직사각형의 한 변의 길이 x를 구하세요."
    return {"problem": problem, "answer": solutions}

def generate_consecutive_odd_problem():
    random_number = random.randint(10, 100)
    largest_square = int((random_number / 3) ** 0.5)
    smallest_odd = largest_square - 2 if largest_square % 2 == 0 else largest_square - 1
    return {"problem": f"연속하는 세 홀수가 있다. 가장 큰 수의 제곱이 다른 두 수의 합보다 {random_number}보다 작을 때 가장 작은 홀수는?", "answer": smallest_odd}

def generate_road_width_problem():
    width = random.randint(1, 20)
    height = random.randint(1, 20)
    grass_area = random.randint(30, 100)
    max_road_width = grass_area // height
    road_width = random.randint(1, max_road_width)
    return {"problem": f"가로와 세로의 길이가 각각 {width}m, {height}m인 잔디밭에 폭이 일정한 길을 내려고 합니다. 길을 제외한 잔디밭의 넓이가 {grass_area}m²입니다. 길의 폭은 얼마입니까?", "answer": road_width}

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