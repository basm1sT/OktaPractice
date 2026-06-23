from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db import crud, db
from app.schemas import CategoryResponse, CategoryCreate, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/", response_model=list[CategoryResponse])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(db.get_db)):
    return crud.get_categories(db, skip=skip, limit=limit)

@router.get("/{category_id}", response_model=CategoryResponse)
def read_category(category_id: int, db: Session = Depends(db.get_db)):
    return crud.get_category(db, category_id)

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, db: Session = Depends(db.get_db)):
    return crud.create_category(db=db, category=category)

@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, category: CategoryUpdate, db: Session = Depends(db.get_db)):
    return crud.update_category(db, category_id, category)

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(db.get_db)):
    crud.delete_category(db, category_id)
    return None