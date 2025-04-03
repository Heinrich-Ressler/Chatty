from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app import schemas, models, database
from fastapi.security import OAuth2PasswordBearer
from typing import List

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)


# Авторизация через OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth_service/login")

# Получить сессию БД
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Получить текущего пользователя (для авторизации)
def get_current_user(token: str = Depends(oauth2_scheme)):
    # Здесь мы можем добавить логику для извлечения пользователя через токен
    return {"user_id": 1}  # Псевдопользователь для теста

# Эндпоинт создания поста
@router.post("/", response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_post = models.Post(**post.dict(), user_id=current_user["user_id"])
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# Эндпоинт получения списка постов
@router.get("/", response_model=List[schemas.Post])
def get_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    posts = db.query(models.Post).offset(skip).limit(limit).all()
    return posts

# Эндпоинт получения одного поста по ID
@router.get("/{post_id}", response_model=schemas.Post)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

# Эндпоинт редактирования поста
@router.put("/{post_id}", response_model=schemas.Post)
def update_post(post_id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.user_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="You are not the author of this post_service")
    db_post.title = post.title
    db_post.content = post.content
    db.commit()
    db.refresh(db_post)
    return db_post

# Эндпоинт удаления поста
@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.user_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="You are not the author of this post_service")
    db.delete(db_post)
    db.commit()
    return {"message": "Post deleted successfully"}
