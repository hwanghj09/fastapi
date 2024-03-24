# model.py

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users_table"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False, unique=True)
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
