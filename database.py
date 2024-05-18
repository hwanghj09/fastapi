from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

USERS_DB_URL = 'mysql+pymysql://root:qwaszx77^^@svc.sel4.cloudtype.app:31168/users'
SHOPPING_DB_URL = 'mysql+pymysql://root:qwaszx77^^@svc.sel4.cloudtype.app:31168/shopping'
DB_URL = 'postgresql+psycopg2://hwanghj09:TZy2fh4gbYku@ep-quiet-water-a2l0cgw1.eu-central-1.pg.koyeb.app/koyebdb'
class Usersengineconn:
    def __init__(self):
        self.engine = create_engine(DB_URL, pool_recycle = 500)
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
        self.engine = create_engine(DB_URL, pool_recycle = 500)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def sessionmaker(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session

    def connection(self):
        conn = self.engine.connect()
        return conn