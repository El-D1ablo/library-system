"""Тесты просмотра списка книг (Issue #2)."""

import unittest

from library_app.catalog import Catalog, CatalogError, format_books


class BookListTests(unittest.TestCase):
    """Проверка Catalog.list_books и format_books."""

    def setUp(self):
        self.catalog = Catalog()
        self.catalog.add_book("5170906319", "Мастер и Маргарита", "Булгаков М.", 1967)
        self.catalog.add_book("5170906320", "Анна Каренина", "Толстой Л.", 1877)
        self.catalog.add_book("5170906321", "Белая гвардия", "Булгаков М.", 1925)

    def test_sorted_by_title_by_default(self):
        titles = [book.title for book in self.catalog.list_books()]
        self.assertEqual(titles, ["Анна Каренина", "Белая гвардия",
                                  "Мастер и Маргарита"])

    def test_sorted_by_year(self):
        years = [book.year for book in self.catalog.list_books("year")]
        self.assertEqual(years, [1877, 1925, 1967])

    def test_sorted_by_author_then_stable(self):
        authors = [book.author for book in self.catalog.list_books("author")]
        self.assertEqual(authors, ["Булгаков М.", "Булгаков М.", "Толстой Л."])

    def test_unknown_sort_field(self):
        with self.assertRaises(CatalogError):
            self.catalog.list_books("price")

    def test_returned_list_does_not_change_catalog(self):
        books = self.catalog.list_books()
        books.clear()
        self.assertEqual(len(self.catalog), 3)

    def test_format_empty_catalog(self):
        self.assertEqual(format_books(Catalog().list_books()), "Каталог пуст")

    def test_format_contains_books(self):
        text = format_books(self.catalog.list_books())
        self.assertIn("Анна Каренина", text)
        self.assertIn("в наличии", text)
        self.assertEqual(len(text.splitlines()), 2 + 3)


if __name__ == "__main__":
    unittest.main()
