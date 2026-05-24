from fastapi import APIRouter, Depends, HTTPException
from ..schemas.user import UserCreateSchema, UserLoginSchema, UserResponseSchema
from passlib.context import CryptContext
from ..dependencies import get_db
from ..models import User
from jose import jwt
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

router = APIRouter(
    prefix="/auth", 
    tags=["auth"]
)

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

@router.post("/register", response_model=UserResponseSchema)
async def register(user: UserCreateSchema, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")

    new_user = User(
        name = user.name,
        email = user.email,
        hashed_password = pwd_context.hash(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
async def login(credentials: UserLoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not pwd_context.verify(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid password")
    payload = {
        "sub": str(user.id),
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return {"access_token": encoded_jwt, "token_type": "bearer"}