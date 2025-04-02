from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.sql.functions import user

import models, schemas
from app.schemas import UserLogin
from app.utils.security import oauth2_sheme
from database import init_db
from utils.security import get_password_hash, authenticate_user, creat_access_token, get_current_user

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(init_db)):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect login or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = creat_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/login", response_model=schemas.UserLogin)
async def login(user_in: schemas.UserLogin, db: AsyncSession = Depends(init_db)):
    token: str = Depends(oauth2_sheme)
    user_in: models = Depends(get_current_user)

    exist_user = await db.execute(select(models.User).filter(models.User.email == user_in.email))
    existing_user = exist_user.scalar_one_or_none()

    if not existing_user:
        raise HTTPException(status_code=400, detail="User not found!")

    return {"token": "your had it, you are Welcome!"}

@router.post("/register", response_model=schemas.UserCreate)
async def register_user(user_in: schemas.UserCreate, db: AsyncSession = Depends(init_db)):
    #проверка на наличие
    exist_user = await db.execute(select(models.User).filter(models.User.email == user_in.email))
    existing_user = exist_user.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = models.User(
        email=user_in.email,
        hashed_password= get_password_hash(exist_user.password)
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user



