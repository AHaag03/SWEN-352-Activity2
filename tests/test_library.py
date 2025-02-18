import unittest
from unittest.mock import Mock
from library import library
import json

from library.patron import Patron

class TestLibrary(unittest.TestCase):
    ############################################################################
    ################################ API METHODS ###############################
    ############################################################################

    def setUp(self):
        self.lib = library.Library()
        with open('tests_data/ebooks.txt', 'r') as f:
            self.books_data = json.loads(f.read())

    def test_is_ebook_true(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)
        self.assertTrue(self.lib.is_ebook('learning python'))

    def test_is_ebook_false(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)
        self.assertFalse(self.lib.is_ebook('non-existent book'))

    def test_get_ebooks_count(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)
        self.assertEqual(self.lib.get_ebooks_count("learning python"), 8)

    def test_is_book_by_author_true(self):
        self.lib.api.books_by_author = Mock(return_value=['learning python'])
        self.assertTrue(self.lib.is_book_by_author('any author', 'learning python'))

    def test_is_book_by_author_false(self):
        self.lib.api.books_by_author = Mock(return_value=[])
        self.assertFalse(self.lib.is_book_by_author('any author', 'learning python'))

    def test_get_languages_for_book(self):
        self.lib.api.get_book_info = Mock(return_value=[{'title': 'learning python', 'publisher': 'penguin', 'publish_year': 2024, 'language': ['english', 'spanish']}])
        self.assertEqual(self.lib.get_languages_for_book('learning python'), {'english', 'spanish'})

    ############################################################################
    ################################# DB METHODS ###############################
    ############################################################################

    def test_register_patron(self):
        patron = Patron('fname', 'lname', '20', '1234')
        self.lib.db.insert_patron = Mock(return_value=patron)
        self.assertTrue(self.lib.register_patron('fname', 'lname', '20', '1234'))

    def test_is_patron_registered_true(self):
        patron = Patron('fname', 'lname', '20', '1234')
        self.lib.db.retrieve_patron = Mock(return_value=patron)
        self.assertTrue(self.lib.is_patron_registered(patron))

    def test_is_patron_registered_false(self):
            patron = Patron('fname', 'lname', '20', '1234')
            self.lib.db.retrieve_patron = Mock(return_value=None)
            self.assertFalse(self.lib.is_patron_registered(patron))

    def test_borrow_book(self):
        patron = Patron('fname', 'lname', '20', '1234')
        book = "Hitchhiker's Guide to the Galaxy"
        self.lib.db.update_patron = Mock(return_value=None)
        self.lib.borrow_book(book, patron)
        self.assertEqual(patron.get_borrowed_books(), [book.lower()])

    def test_return_borrowed_book(self):
        patron = Patron('fname', 'lname', '20', '1234')
        book = "Hitchhiker's Guide to the Galaxy"
        self.lib.db.update_patron = Mock(return_value=None)
        self.lib.return_borrowed_book(book, patron)
        self.assertEqual(patron.get_borrowed_books(), [])

    def test_is_book_borrowed_true(self):
        patron = Patron('fname', 'lname', '20', '1234')
        book = "Hitchhiker's Guide to the Galaxy".lower()
        patron.get_borrowed_books = Mock(return_value=[book])
        self.assertTrue(self.lib.is_book_borrowed(book, patron))

    def test_is_book_borrowed_false(self):
        patron = Patron('fname', 'lname', '20', '1234')
        book = "Hitchhiker's Guide to the Galaxy"
        patron.get_borrowed_books = Mock(return_value=[])
        self.assertFalse(self.lib.is_book_borrowed(book, patron))
