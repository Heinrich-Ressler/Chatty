from sqlalchemy.orm import Session
from . import models, schemas

# Посты
def create_post(db: Session, post: schemas.PostCreate):
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_post(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()

def get_all_posts(db: Session):
    return db.query(models.Post).all()

def update_post(db: Session, post_id: int, post: schemas.PostUpdate):
    db_post = get_post(db, post_id)
    if db_post:
        for key, value in post.dict().items():
            setattr(db_post, key, value)
        db.commit()
        db.refresh(db_post)
    return db_post

def delete_post(db: Session, post_id: int):
    db_post = get_post(db, post_id)
    if db_post:
        db.delete(db_post)
        db.commit()
    return db_post


# Комментарии
def create_comment(db: Session, comment: schemas.CommentCreate):
    db_comment = models.Comment(**comment.dict())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comments_by_post(db: Session, post_id: int):
    return db.query(models.Comment).filter(models.Comment.post_id == post_id).all()

def update_comment(db: Session, comment_id: int, content: str):
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if comment:
        comment.content = content
        db.commit()
        db.refresh(comment)
    return comment

def delete_comment(db: Session, comment_id: int):
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if comment:
        db.delete(comment)
        db.commit()
    return comment


# Лайки
def like_post(db: Session, post_id: int, user_id: int):
    existing_like = db.query(models.Like).filter_by(post_id=post_id, user_id=user_id).first()
    if existing_like:
        return None  # Уже лайкал
    like = models.Like(post_id=post_id, user_id=user_id)
    db.add(like)
    db.commit()
    db.refresh(like)
    return like

def unlike_post(db: Session, post_id: int, user_id: int):
    like = db.query(models.Like).filter_by(post_id=post_id, user_id=user_id).first()
    if like:
        db.delete(like)
        db.commit()
    return like
