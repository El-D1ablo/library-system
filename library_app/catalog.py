"""Каталог книг библиотеки."""

from __future__ import annotations

from datetime import date
from typing import Dict, List, Union

from library_app.models import Book

MIN_YEAR = 1450  # первые печатные книги
SORT_FIELDS = ("title", "author", "year")


class CatalogError(ValueError):
    """Ошибка работы с каталогом: некорректные данные или повтор ISBN."""


def normalize_isbn(isbn: str) -> str:
    """Приводит ISBN к единому виду: убирает пробелы и дефисы.

    Args:
        isbn: ISBN в том виде, в котором его ввёл пользователь.

    Returns:
        Строка из цифр без пробелов и дефисов.
    """
    return isbn.replace("-", "").replace(" ", "").strip()


class Catalog:
    """Каталог книг. Книги хранятся в памяти, ключ — ISBN."""

    def __init__(self) -> None:
        """Создаёт пустой каталог."""
        self._books: Dict[str, Book] = {}

    def __len__(self) -> int:
        """Возвращает количество книг в каталоге."""
        return len(self._books)

    def add_book(self, isbn: str, title: str, author: str,
                 year: Union[int, str]) -> Book:
        """Добавляет новую книгу в каталог после проверки данных.

        Args:
            isbn: ISBN книги, 10 или 13 цифр (дефисы и пробелы допускаются).
            title: Название книги, не пустое.
            author: Автор книги, не пустой.
            year: Год издания — число от 1450 до текущего года.

        Returns:
            Добавленная книга (объект Book).

        Raises:
            CatalogError: если данные некорректны или книга с таким ISBN
                уже есть в каталоге.
        """
        isbn = normalize_isbn(isbn)
        title = title.strip()
        author = author.strip()

        if not (isbn.isdigit() and len(isbn) in (10, 13)):
            raise CatalogError("ISBN должен содержать 10 или 13 цифр")
        if not title:
            raise CatalogError("Название книги не может быть пустым")
        if not author:
            raise CatalogError("Автор книги не может быть пустым")
        try:
            year = int(year)
        except (TypeError, ValueError):
            raise CatalogError("Год издания должен быть целым числом") from None
        current_year = date.today().year
        if not MIN_YEAR <= year <= current_year:
            raise CatalogError(
                f"Год издания должен быть от {MIN_YEAR} до {current_year}")
        if isbn in self._books:
            raise CatalogError(f"Книга с ISBN {isbn} уже есть в каталоге")

        book = Book(isbn=isbn, title=title, author=author, year=year)
        self._books[isbn] = book
        return book

    def list_books(self, sort_by: str = "title") -> List[Book]:
        """Возвращает список всех книг каталога, отсортированный по полю.

        Args:
            sort_by: Поле сортировки: "title" (по названию, по умолчанию),
                "author" (по автору) или "year" (по году издания).

        Returns:
            Новый список книг; изменение списка не меняет каталог.

        Raises:
            CatalogError: если указано неизвестное поле сортировки.
        """
        if sort_by not in SORT_FIELDS:
            raise CatalogError(
                f"Сортировка возможна только по полям: {', '.join(SORT_FIELDS)}")
        if sort_by == "year":
            key = lambda book: (book.year, book.title.lower())
        else:
            key = lambda book: getattr(book, sort_by).lower()
        return sorted(self._books.values(), key=key)


def format_books(books: List[Book]) -> str:
    """Формирует таблицу книг для вывода в консоль.

    Args:
        books: Список книг для вывода.

    Returns:
        Текст таблицы с колонками №, ISBN, название, автор, год, статус;
        если список пуст — сообщение «Каталог пуст».
    """
    if not books:
        return "Каталог пуст"
    header = f"{'№':>3}  {'ISBN':<13}  {'Название':<30}  {'Автор':<20}  {'Год':>4}  Статус"
    lines = [header, "-" * len(header)]
    for number, book in enumerate(books, start=1):
        status = "в наличии" if book.available else "выдана"
        lines.append(f"{number:>3}  {book.isbn:<13}  {book.title[:30]:<30}  "
                     f"{book.author[:20]:<20}  {book.year:>4}  {status}")
    return "\n".join(lines)
