from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users_table"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    
class Inquiry(Base):
    __tablename__ = "inquiry"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)  # 이름 열을 username으로 수정
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
