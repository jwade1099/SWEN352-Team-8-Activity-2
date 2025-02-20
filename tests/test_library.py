import unittest
from unittest.mock import Mock
from library import library
import json

class TestLibrary(unittest.TestCase):

    def setUp(self):
        self.lib = library.Library()
        library.Patron = Mock()
        self.ebooks_data = [{"title": "Learning Python", "ebook_count": 3}, {"title": "Learning Python (Learning)", "ebook_count": 1}, {"title": "Learning Python", "ebook_count": 1}, {"title": "Learn to Program Using Python", "ebook_count": 1}, {"title": "Aprendendo Python", "ebook_count": 1}, {"title": "Python Basics", "ebook_count": 1}]
        self.book_titles = ["Learning Python", "Learning Python (Learning)", "Learn to Program Using Python", "Aprendendo Python", "Python Basics"]

    def test_is_ebook_true(self):
        self.lib.api.get_ebooks = Mock(return_value=self.ebooks_data)
        self.assertTrue(self.lib.is_ebook('learning python'))

    def test_is_ebook_false(self):
        self.lib.api.get_ebooks = Mock(return_value=self.ebooks_data)
        self.assertFalse(self.lib.is_ebook('learning java'))

    def test_get_ebooks_count(self):
        self.lib.api.get_ebooks = Mock(return_value=self.ebooks_data)
        self.assertEqual(self.lib.get_ebooks_count("learning python"), 8)

    def test_get_ebooks_count_zero(self):
        self.lib.api.get_ebooks = Mock(return_value=[])
        self.assertEqual(self.lib.get_ebooks_count("learning java"), 0)

    def test_is_book_by_author_true(self):
        self.lib.api.books_by_author = Mock(return_value=self.book_titles)
        self.assertTrue(self.lib.is_book_by_author("Aurelian", "learning python"))

    def test_is_book_by_author_false(self):
        self.lib.api.books_by_author = Mock(return_value=self.book_titles)
        self.assertFalse(self.lib.is_book_by_author("Aurelian", "learning java"))

    def test_get_languages_for_book(self):
        self.lib.api.get_book_info = Mock(return_value=[{"language": {"english", "russian"}}])
        self.assertEqual(self.lib.get_languages_for_book("book"), {"english", "russian"})

    def test_register_patron(self):
        self.lib.db.insert_patron = Mock(return_value=10)
        self.assertEqual(self.lib.register_patron("Friedrich", "Nietzsche", "21", "10"), 10)

    def test_register_patron_exists(self):
        self.lib.db.insert_patron = Mock(return_value=None)
        self.assertEqual(self.lib.register_patron("Friedrich", "Nietzsche", "21", "10"), None)
    
    def test_is_patron_registered_true(self):
        new_patron = library.Patron()
        self.lib.db.retrieve_patron = Mock(return_value=new_patron)
        self.assertTrue(self.lib.is_patron_registered(new_patron))

    def test_is_patron_registered_false(self):
        new_patron = library.Patron()
        self.lib.db.retrieve_patron = Mock(return_value=None)
        self.assertFalse(self.lib.is_patron_registered(new_patron))

    def test_borrow_book(self):
        new_patron = library.Patron()
        new_patron.add_borrowed_book = Mock()
        self.lib.db.update_patron = Mock()
        self.lib.borrow_book("Rejected", new_patron)
        new_patron.add_borrowed_book.assert_called()
        self.lib.db.update_patron.assert_called()
        
    def test_return_borrowed_book(self):
        new_patron = library.Patron()
        new_patron.return_borrowed_book = Mock()
        self.lib.db.update_patron = Mock()
        self.lib.return_borrowed_book("Rejected", new_patron)
        new_patron.return_borrowed_book.assert_called()
        self.lib.db.update_patron.assert_called()

    def test_is_book_borrowed_true(self):
        new_patron = library.Patron()
        new_patron.get_borrowed_books = Mock(return_value=["rome"])
        self.assertTrue(self.lib.is_book_borrowed("rome", new_patron))

    def test_is_book_borrowed_false(self):
        new_patron = library.Patron()
        new_patron.get_borrowed_books = Mock(return_value=[])
        self.assertFalse(self.lib.is_book_borrowed("rome", new_patron))