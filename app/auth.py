from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.database import get_db
from app.utils.security import authenticate_user, create_access_token, get_password_hash, get_current_user
from app.schemas import EmailPasswordForm  # Кастомная форма
from app import models, schemas


from sqlalchemy import select

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.post("/token",summary="получи Токен", description="Введи свой маил, и пароль" )
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(401, "Неверные логин или пароль")


    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )


    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/verify", summary="проверь подключен ли Токен", description="Если Токен подключён, увидишь свой маил")
async def verify_token(
        user: models.User = Depends(get_current_user)
):

    return {"username": user.email}



@router.post(
    "/register",
    response_model=schemas.UserRead,
    summary="Регистрация нового пользователя",
    description="Создание нового пользователя по email и паролю. Email должен быть уникальным."
)
async def register_user(
    user_in: schemas.UserCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(models.User).filter(models.User.email == user_in.email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = models.User(
        email=user_in.email,
        password_hash=get_password_hash(user_in.password),
        nickname=user_in.nickname
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user

