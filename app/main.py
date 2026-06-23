from fastapi import FastAPI
from app.api import books, categories
from app.db.db import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Book API", version="1.0.0")

app.include_router(books.router)
app.include_router(categories.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}