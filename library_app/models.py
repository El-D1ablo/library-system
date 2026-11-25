"""Модели данных библиотечной системы."""

from dataclasses import dataclass


@dataclass
class Book:
    """Книга в каталоге библиотеки.

    Attributes:
        isbn: Уникальный номер книги (ISBN) — 10 или 13 цифр без дефисов.
        title: Название книги.
        author: Автор книги.
        year: Год издания.
        available: True, если книга находится в библиотеке и её можно выдать.
    """

    isbn: str
    title: str
    author: str
    year: int
    available: bool = True
