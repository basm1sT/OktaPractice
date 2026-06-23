from sqlalchemy.orm import Session
from . import models
from typing import List, Optional

def create_category(db: Session, title: str):
    category = models.Category(title=title)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def get_categories(db: Session, skip: int = 0, limit: int = 100) -> List[models.Category]:
    return db.query(models.Category).offset(skip).limit(limit).all()


def get_category(db: Session, category_id: int) -> Optional[models.Category]:
    return db.query(models.Category).filter(models.Category.id == category_id).first()


def get_category_by_title(db: Session, title: str) -> Optional[models.Category]:
    return db.query(models.Category).filter(models.Category.title == title).first()


def delete_category(db: Session, category_id: int) -> bool:
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if category:
        db.delete(category)
        db.commit()
        return True
    return False

def create_book(db: Session, title: str, description: str = None, 
                price: float = 0.0, url: str = None, category_id: int = None):
    book = models.Book(
        title=title,
        description=description,
        price=price,
        url=url,
        category_id=category_id
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def get_books(db: Session, skip: int = 0, limit: int = 100) -> List[models.Book]:
    return db.query(models.Book).offset(skip).limit(limit).all()


def get_book(db: Session, book_id: int) -> Optional[models.Book]:
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_books_by_category(db: Session, category_id: int, skip: int = 0, limit: int = 100) -> List[models.Book]:
    return db.query(models.Book)\
              .filter(models.Book.category_id == category_id)\
              .offset(skip).limit(limit).all()


def update_book(db: Session, book_id: int, **kwargs):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        return None
    
    for key, value in kwargs.items():
        if value is not None and hasattr(book, key):
            setattr(book, key, value)
    
    db.commit()
    db.refresh(book)
    return book


def delete_book(db: Session, book_id: int) -> bool:
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book:
        db.delete(book)
        db.commit()
        return True
    return False