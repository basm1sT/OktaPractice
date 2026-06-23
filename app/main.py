from app.db.db import SessionLocal
from app.db.crud import get_categories, get_books

def main():
    db = SessionLocal()
    try:
        print("=== КАТЕГОРИИ ===")
        categories = get_categories(db)
        for cat in categories:
            print(f"ID: {cat.id} | {cat.title}")

        print("\n=== КНИГИ ===")
        books = get_books(db)
        for book in books:
            print(f"ID: {book.id} | '{book.title}' | Цена: {float(book.price)} руб. | Категория: {book.category_id}")

        print(f"\nВсего категорий: {len(categories)}")
        print(f"Всего книг: {len(books)}")

    finally:
        db.close()

if __name__ == "__main__":
    main()
