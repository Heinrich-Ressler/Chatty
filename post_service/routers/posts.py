from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal
import os
from fastapi import UploadFile, File
from uuid import uuid4

router = APIRouter()

# Зависимость — подключение к БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----- Посты -----

@router.post("/posts/", response_model=schemas.PostOut)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    return crud.create_post(db, post)

@router.get("/posts/", response_model=list[schemas.PostOut])
def read_all_posts(db: Session = Depends(get_db)):
    return crud.get_all_posts(db)

@router.get("/posts/{post_id}", response_model=schemas.PostOut)
def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.get_post(db, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Пост не найден")
    return db_post

@router.put("/posts/{post_id}", response_model=schemas.PostOut)
def update_post(post_id: int, post: schemas.PostUpdate, db: Session = Depends(get_db)):
    return crud.update_post(db, post_id, post)

@router.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    return crud.delete_post(db, post_id)

# ----- Комментарии -----

@router.post("/comments/", response_model=schemas.CommentOut)
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    return crud.create_comment(db, comment)

@router.get("/posts/{post_id}/comments", response_model=list[schemas.CommentOut])
def get_comments(post_id: int, db: Session = Depends(get_db)):
    return crud.get_comments_by_post(db, post_id)

@router.put("/comments/{comment_id}", response_model=schemas.CommentOut)
def update_comment(comment_id: int, comment: schemas.CommentUpdate, db: Session = Depends(get_db)):
    return crud.update_comment(db, comment_id, comment.content)

@router.delete("/comments/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    return crud.delete_comment(db, comment_id)

# ----- Лайки -----

@router.post("/posts/{post_id}/like")
def like(post_id: int, user_id: int, db: Session = Depends(get_db)):
    result = crud.like_post(db, post_id, user_id)
    if not result:
        raise HTTPException(status_code=400, detail="Уже лайкнуто")
    return {"message": "Лайк добавлен"}

@router.delete("/posts/{post_id}/like")
def unlike(post_id: int, user_id: int, db: Session = Depends(get_db)):
    result = crud.unlike_post(db, post_id, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="Лайк не найден")
    return {"message": "Лайк удалён"}



UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.post("/posts/{post_id}/upload-image")
def upload_image(post_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    post = crud.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")

    file_ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid4().hex}{file_ext}"
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    post.image_url = f"/{UPLOAD_FOLDER}/{filename}"
    db.commit()
    db.refresh(post)

    return {"message": "Изображение загружено", "image_url": post.image_url}