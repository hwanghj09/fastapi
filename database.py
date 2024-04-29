from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

USERS_DB_URL = 'mysql+pymysql://root:qwaszx77^^@svc.sel4.cloudtype.app:31168/users'
SHOPPING_DB_URL = 'mysql+pymysql://root:qwaszx77^^@svc.sel4.cloudtype.app:31168/shopping'

class Usersengineconn:
    def __init__(self):
        self.engine = create_engine(USERS_DB_URL, pool_recycle = 500)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def sessionmaker(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session

    def connection(self):
        conn = self.engine.connect()
        return conn
        
class Shoppingengineconn:
    def __init__(self):
        self.engine = create_engine(SHOPPING_DB_URL, pool_recycle = 500)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def sessionmaker(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session

    def connection(self):
        conn = self.engine.connect()
        return conn