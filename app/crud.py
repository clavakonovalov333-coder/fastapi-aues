from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Users
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed = pwd_context.hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed, full_name=user.full_name, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user: 
        return None
    if not pwd_context.verify(password, user.hashed_password):
        return None
    return user

def list_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# Subjects
def create_subject(db: Session, subject: schemas.SubjectCreate):
    db_item = models.Subject(code=subject.code, title=subject.title, description=subject.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_subject(db: Session, subject_id: int):
    return db.query(models.Subject).get(subject_id)

def list_subjects(db: Session):
    return db.query(models.Subject).all()

# Teachers
def create_teacher(db: Session, teacher: schemas.TeacherCreate):
    t = models.Teacher(name=teacher.name, bio=teacher.bio, email=teacher.email, phone=teacher.phone)
    if teacher.subject_ids:
        subjects = db.query(models.Subject).filter(models.Subject.id.in_(teacher.subject_ids)).all()
        t.subjects = subjects
    db.add(t)
    db.commit()
    db.refresh(t)
    return t

def list_teachers(db: Session):
    return db.query(models.Teacher).all()

def get_teacher(db: Session, teacher_id: int):
    return db.query(models.Teacher).get(teacher_id)

def assign_subjects_to_teacher(db: Session, teacher_id: int, subject_ids: list[int]):
    t = get_teacher(db, teacher_id)
    if not t:
        return None
    subjects = db.query(models.Subject).filter(models.Subject.id.in_(subject_ids)).all()
    t.subjects = subjects
    db.add(t)
    db.commit()
    db.refresh(t)
    return t