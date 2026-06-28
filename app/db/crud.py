from sqlalchemy.orm import Session
from . import models
from typing import List, Optional
from fastapi import HTTPException, status
from app.schemas import BookCreate, BookUpdate, CategoryCreate, CategoryUpdate

def create_category(db: Session, category: CategoryCreate):
    existing = db.query(models.Category).filter(models.Category.title == category.title).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category with same title exists")
    db_category = models.Category(title=category.title)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_categories(db: Session, skip: int = 0, limit: int = 100) -> List[models.Category]:
    return db.query(models.Category).offset(skip).limit(limit).all()

def get_category(db: Session, category_id: int) -> Optional[models.Category]:
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def get_category_by_title(db: Session, title: str) -> Optional[models.Category]:
    return db.query(models.Category).filter(models.Category.title == title).first()

def update_category(db: Session, category_id: int, category: CategoryUpdate) -> Optional[models.Category]:
    db_category = get_category(db, category_id)
    if not db_category:
        return None
    if category.title is not None:
        existing = db.query(models.Category).filter(
            models.Category.title == category.title,
            models.Category.id != category_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Category with same title exists")
        db_category.title = category.title
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int) -> bool:
    category = get_category(db, category_id)
    if not category:
        return False
    db.delete(category)
    db.commit()
    return True

def create_book(db: Session, book: BookCreate) -> models.Book:
    category = get_category(db, book.category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    db_book = models.Book(
        title=book.title,
        description=book.description,
        price=book.price,
        url=book.url,
        category_id=book.category_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_books(db: Session, skip: int = 0, limit: int = 100) -> List[models.Book]:
    return db.query(models.Book).offset(skip).limit(limit).all()

def get_book(db: Session, book_id: int) -> Optional[models.Book]:
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_books_by_category(db: Session, category_id: int, skip: int = 0, limit: int = 100) -> List[models.Book]:
    return db.query(models.Book).filter(models.Book.category_id == category_id).offset(skip).limit(limit).all()

def update_book(db: Session, book_id: int, book: BookUpdate) -> Optional[models.Book]:
    db_book = get_book(db, book_id)
    if not db_book:
        return None
    
    if book.category_id is not None:
        category = get_category(db, book.category_id)
        if not category:
            raise HTTPException(status_code=404, detail="New category not found")
        db_book.category_id = book.category_id
    
    if book.title is not None:
        db_book.title = book.title
    if book.description is not None:
        db_book.description = book.description
    if book.price is not None:
        db_book.price = book.price
    if book.url is not None:
        db_book.url = book.url
    
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int) -> bool:
    book = get_book(db, book_id)
    if not book:
        return False
    db.delete(book)
    db.commit()
    return True