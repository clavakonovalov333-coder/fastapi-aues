from sqlalchemy import Column, Integer, String, Text, Table, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base

# связь учителя и предметов
teacher_subject = Table(
    "teacher_subject",
    Base.metadata,
    Column("teacher_id", Integer, ForeignKey("teachers.id"), primary_key=True),
    Column("subject_id", Integer, ForeignKey("subjects.id"), primary_key=True),
)

class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    body = Column(Text, nullable=True)
    date = Column(String(20), nullable=True)

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    desc = Column(Text, nullable=True)

class AdminMember(Base):
    __tablename__ = "admin_members"
    id = Column(Integer, primary_key=True, index=True)
    position = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    photo = Column(String(255), nullable=True)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    role = Column(String(50), default="EDITOR")  # SUPERADMIN / ADMIN / EDITOR

class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    bio = Column(Text, nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    subjects = relationship("Subject", secondary=teacher_subject, back_populates="teachers")

class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(64), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    teachers = relationship("Teacher", secondary=teacher_subject, back_populates="subjects")