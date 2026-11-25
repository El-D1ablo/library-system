"""Тесты добавления книги в каталог (Issue #1)."""

import unittest
from datetime import date

from library_app.catalog import Catalog, CatalogError


class AddBookTests(unittest.TestCase):
    """Проверка метода Catalog.add_book."""

    def setUp(self):
        self.catalog = Catalog()

    def test_add_valid_book(self):
        book = self.catalog.add_book("978-5-17-090631-9", "Мастер и Маргарита",
                                     "М. Булгаков", "1967")
        self.assertEqual(book.isbn, "9785170906319")
        self.assertEqual(book.year, 1967)
        self.assertTrue(book.available)
        self.assertEqual(len(self.catalog), 1)

    def test_spaces_are_trimmed(self):
        book = self.catalog.add_book(" 5170906319 ", "  Война и мир ",
                                     " Л. Толстой ", 1869)
        self.assertEqual(book.title, "Война и мир")
        self.assertEqual(book.author, "Л. Толстой")

    def test_duplicate_isbn_rejected(self):
        self.catalog.add_book("5170906319", "Книга", "Автор", 2000)
        with self.assertRaises(CatalogError):
            self.catalog.add_book("517-090-631-9", "Другая", "Автор", 2001)
        self.assertEqual(len(self.catalog), 1)

    def test_invalid_isbn(self):
        for isbn in ("", "12345", "97851709063AB", "12345678901"):
            with self.subTest(isbn=isbn), self.assertRaises(CatalogError):
                self.catalog.add_book(isbn, "Книга", "Автор", 2000)

    def test_empty_title_or_author(self):
        with self.assertRaises(CatalogError):
            self.catalog.add_book("5170906319", "   ", "Автор", 2000)
        with self.assertRaises(CatalogError):
            self.catalog.add_book("5170906319", "Книга", "", 2000)

    def test_invalid_year(self):
        next_year = date.today().year + 1
        for year in ("две тысячи", "", 1000, next_year):
            with self.subTest(year=year), self.assertRaises(CatalogError):
                self.catalog.add_book("5170906319", "Книга", "Автор", year)
        self.assertEqual(len(self.catalog), 0)


if __name__ == "__main__":
    unittest.main()
