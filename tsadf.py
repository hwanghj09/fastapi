import psycopg2

# PostgreSQL 연결 정보
DB_CONFIG = {
    "host": "dpg-cp4pc6q1hbls73f4lf80-a.oregon-postgres.render.com",
    "database": "db_fahq",
    "user": "hwanghj09",
    "password": "ru0U1ZfFZvtR5ppaKbr85ZqjDZL5tcmo"
}

def execute_query(query):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def fetch_table_data(table_name):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    table_data = cursor.fetchall()
    return cursor, table_data


def initialize_tables():
    initialize_query = """
    DELETE FROM users_table;
    DELETE FROM inquiry;
    DELETE FROM board;
    DELETE FROM products;
    """
    execute_query(initialize_query)

    # 사용할 테이블 생성
    create_users_table_query = """
    CREATE TABLE IF NOT EXISTS users_table (
        id serial not null primary key,
        name VARCHAR(20),
        password VARCHAR(100)
    );
    """
    execute_query(create_users_table_query)

    create_inquiry_table_query = """
    CREATE TABLE IF NOT EXISTS inquiry (
        id serial not null primary key,
        title VARCHAR(255),
        username VARCHAR(255),
        content TEXT
    );
    """
    execute_query(create_inquiry_table_query)

    create_board_table_query = """
    CREATE TABLE IF NOT EXISTS board (
        id serial not null primary key,
        title VARCHAR(255) NOT NULL,
        content TEXT NOT NULL,
        author VARCHAR(100) NOT NULL
    );
    """
    execute_query(create_board_table_query)

    create_products_table_query = """
    CREATE TABLE IF NOT EXISTS products (
        id serial not null primary key,
        name VARCHAR(255) NOT NULL,
        price DECIMAL(10, 2) NOT NULL,
        image_url VARCHAR(255) NOT NULL
    );
    """
    execute_query(create_products_table_query)

    # 데이터 삽입
    insert_product_query = """
    INSERT INTO products (name, price, image_url) VALUES ('상품', 3.14159265643264235754385428746856, 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTliEeZrjb6wyU1W9sA1vZSar4p8yt0rp_h_G2tRao6iA&s');
    """
    execute_query(insert_product_query)

    print("테이블 생성 및 초기 데이터 삽입이 완료되었습니다.")

def print_table_data(table_name):
    cursor, table_data = fetch_table_data(table_name)  # 수정된 부분
    # 각 컬럼의 최대 길이 계산
    max_column_lengths = [max(len(str(cell)) for cell in row) for row in zip(*table_data)]
    # 컬럼명 출력
    column_names = [desc[0] for desc in cursor.description]
    print(f"{table_name} 데이터:")
    print(" | ".join(f"{name:<{length}}" for name, length in zip(column_names, max_column_lengths)))
    print("-" * (sum(max_column_lengths) + len(max_column_lengths) - 1))
    # 데이터 출력
    for row in table_data:
        print(" | ".join(f"{str(cell):<{length}}" for cell, length in zip(row, max_column_lengths)))

while True:
    # 사용자 입력에 따라 실행할 동작 선택
    print("실행할 동작을 선택하세요:")
    print("1. 테이블 초기화 및 데이터 삽입")
    print("2. users_table 데이터 출력")
    print("3. inquiry 테이블 데이터 출력")
    print("4. board 테이블 데이터 출력")
    print("5. products 테이블 데이터 출력")
    choice = input("선택: ")

    if choice == "1":
        initialize_tables()
    elif choice == "2":
        print_table_data("users_table")
    elif choice == "3":
        print_table_data("inquiry")
    elif choice == "4":
        print_table_data("board")
    elif choice == "5":
        print_table_data("products")
    else:
        print("올바른 선택이 아닙니다. 프로그램을 종료합니다.")
