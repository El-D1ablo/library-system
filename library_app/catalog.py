"""Каталог книг библиотеки."""

from __future__ import annotations

from datetime import date
from typing import Dict, Union

from library_app.models import Book

MIN_YEAR = 1450  # первые печатные книги


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
