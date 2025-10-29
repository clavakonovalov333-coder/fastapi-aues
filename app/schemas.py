from pydantic import BaseModel, EmailStr
from typing import Optional, List

# Auth / Token
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None

# User
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    role: Optional[str] = "EDITOR"

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    is_active: bool
    class Config:
        orm_mode = True

# Teacher / Subject
class SubjectBase(BaseModel):
    code: str
    title: str
    description: Optional[str] = None

class SubjectCreate(SubjectBase):
    pass

class SubjectOut(SubjectBase):
    id: int
    class Config:
        orm_mode = True

class TeacherBase(BaseModel):
    name: str
    bio: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

class TeacherCreate(TeacherBase):
    subject_ids: Optional[List[int]] = []

class TeacherOut(TeacherBase):
    id: int
    subjects: List[SubjectOut] = []
    class Config:
        orm_mode = True