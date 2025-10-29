from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, get_db, Base
from .auth import create_access_token, require_role

# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AUES Admin API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth token
@app.post("/auth/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token_data = {"sub": user.email, "role": user.role}
    access_token = create_access_token(token_data)
    return {"access_token": access_token, "token_type": "bearer"}

# Users (SUPERADMIN and ADMIN allowed for management)
@app.post("/api/users", response_model=schemas.UserOut, dependencies=[Depends(require_role(["SUPERADMIN","ADMIN"]))])
def api_create_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = crud.create_user(db, user_in)
    return user

@app.get("/api/users", response_model=list[schemas.UserOut], dependencies=[Depends(require_role(["SUPERADMIN","ADMIN"]))])
def api_list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_users(db, skip=skip, limit=limit)

# Subjects
@app.post("/api/subjects", response_model=schemas.SubjectOut, dependencies=[Depends(require_role(["SUPERADMIN","ADMIN"]))])
def api_create_subject(subject: schemas.SubjectCreate, db: Session = Depends(get_db)):
    return crud.create_subject(db, subject)

@app.get("/api/subjects", response_model=list[schemas.SubjectOut], dependencies=[Depends(require_role(["SUPERADMIN","ADMIN","EDITOR"]))])
def api_list_subjects(db: Session = Depends(get_db)):
    return crud.list_subjects(db)

# Teachers
@app.post("/api/teachers", response_model=schemas.TeacherOut, dependencies=[Depends(require_role(["SUPERADMIN","ADMIN","EDITOR"]))])
def api_create_teacher(t: schemas.TeacherCreate, db: Session = Depends(get_db)):
    return crud.create_teacher(db, t)

@app.get("/api/teachers", response_model=list[schemas.TeacherOut], dependencies=[Depends(require_role(["SUPERADMIN","ADMIN","EDITOR"]))])
def api_list_teachers(db: Session = Depends(get_db)):
    return crud.list_teachers(db)