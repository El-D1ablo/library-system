"""Точка входа: консольное меню библиотечной системы."""

from library_app.catalog import Catalog, CatalogError, format_books


def add_book_dialog(catalog: Catalog) -> None:
    """Запрашивает у пользователя данные книги и добавляет её в каталог.

    Args:
        catalog: Каталог, в который добавляется книга.
    """
    isbn = input("ISBN: ")
    title = input("Название: ")
    author = input("Автор: ")
    year = input("Год издания: ")
    try:
        book = catalog.add_book(isbn, title, author, year)
    except CatalogError as error:
        print(f"Ошибка: {error}")
    else:
        print(f"Книга «{book.title}» добавлена. Всего книг: {len(catalog)}")


def list_books_dialog(catalog: Catalog) -> None:
    """Спрашивает поле сортировки и выводит список книг каталога.

    Args:
        catalog: Каталог, книги которого выводятся.
    """
    print("Сортировать по: 1 — названию, 2 — автору, 3 — году")
    fields = {"1": "title", "2": "author", "3": "year", "": "title"}
    sort_by = fields.get(input("Ваш выбор (Enter — по названию): ").strip())
    if sort_by is None:
        print("Ошибка: нет такого варианта сортировки")
        return
    print(format_books(catalog.list_books(sort_by)))


def main() -> None:
    """Запускает главное меню программы."""
    catalog = Catalog()
    while True:
        print("\n=== Библиотечная система ===")
        print("1 — Добавить книгу")
        print("2 — Список книг")
        print("0 — Выход")
        choice = input("Выберите пункт: ").strip()
        if choice == "1":
            add_book_dialog(catalog)
        elif choice == "2":
            list_books_dialog(catalog)
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Нет такого пункта меню")


if __name__ == "__main__":
    main()
