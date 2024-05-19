import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

class Usersengineconn:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="dpg-cp4pc6q1hbls73f4lf80-a.oregon-postgres.render.com",
            database="db_fahq",
            user="hwanghj09",
            password="ru0U1ZfFZvtR5ppaKbr85ZqjDZL5tcmo"
        )

    def sessionmaker(self):
        return self.conn

class Shoppingengineconn:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="dpg-cp4pc6q1hbls73f4lf80-a.oregon-postgres.render.com",
            database="db_fahq",
            user="hwanghj09",
            password="ru0U1ZfFZvtR5ppaKbr85ZqjDZL5tcmo"
        )

    def sessionmaker(self):
        return self.conn
