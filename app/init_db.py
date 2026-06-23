from sqlalchemy.orm import Session
from app.db.db import SessionLocal, engine
from app.db.models import Base
from app.db.crud import create_category, create_book

def init_db():
    # Создаём таблицы
    Base.metadata.create_all(bind=engine)
    print("Таблицы books и categories успешно созданы!")

    db: Session = SessionLocal()
    try:
        # Добавляем 2 категории
        print("\nДобавляем категории...")
        cat1 = create_category(db, "Художественная литература")
        cat2 = create_category(db, "Техническая литература")

        print("Добавляем книги...")

        create_book(db, "1984", "Дистопия Джорджа Оруэлла", 450.00, "", cat1.id)
        create_book(db, "Мастер и Маргарита", "Классика Михаила Булгакова", 520.00, "", cat1.id)
        create_book(db, "Преступление и наказание", "Роман Фёдора Достоевского", 380.00, "", cat1.id)
        create_book(db, "Гарри Поттер и Философский камень", "Фэнтези Дж. К. Роулинг", 650.00, "", cat1.id)

        create_book(db, "Чистый код", "Руководство по написанию качественного кода", 890.00, "", cat2.id)
        create_book(db, "Python для начинающих", "Отличная книга для старта в программировании", 720.00, "", cat2.id)
        create_book(db, "Структура и интерпретация компьютерных программ", "Классика компьютерных наук", 1250.00, "", cat2.id)

        print("Инициализация базы данных завершена!")
        print(f"Добавлено 2 категории и 7 книг.")

    finally:
        db.close()

if __name__ == "__main__":
    init_db()
