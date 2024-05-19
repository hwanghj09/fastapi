from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users_table"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

class Inquiry(Base):
    __tablename__ = "inquiry"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)

class Board(Base):
    __tablename__ = "board"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    image_url = Column(String)
