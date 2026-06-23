from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.db import crud, db
from app.schemas import BookResponse, BookCreate, BookUpdate

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/", response_model=list[BookResponse])
def read_books(
    category_id: int = Query(None, description="Filter by category ID"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(db.get_db)
):
    if category_id is not None:
        return crud.get_books_by_category(db, category_id=category_id, skip=skip, limit=limit)
    return crud.get_books(db, skip=skip, limit=limit)

@router.get("/{book_id}", response_model=BookResponse)
def read_book(book_id: int, db: Session = Depends(db.get_db)):
    return crud.get_book(db, book_id)

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db: Session = Depends(db.get_db)):
    return crud.create_book(db=db, book=book)

@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book: BookUpdate, db: Session = Depends(db.get_db)):
    return crud.update_book(db, book_id, book)

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(db.get_db)):
    crud.delete_book(db, book_id)
    return None