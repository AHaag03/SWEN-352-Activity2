import unittest
from library import patron

class TestPatron(unittest.TestCase):

    def setUp(self):
        self.pat = patron.Patron('fname', 'lname', '20', '1234')

    def test_valid_name(self):
        pat = patron.Patron('fname', 'lname', '20', '1234')
        self.assertTrue(isinstance(pat, patron.Patron))

    def test_invalid_name(self):
        self.assertRaises(patron.InvalidNameException, patron.Patron, '1fname', '1lname', '20', '1234')

    def test_add_borrowed_book(self):
        name = 'Hitchhikers Guide to the Galaxy'
        self.pat.add_borrowed_book(name)
        self.assertEqual(self.pat.borrowed_books, [name.lower()])

        self.pat.borrowed_books.remove(name.lower())

    def test_add_borrowed_book_already_borrowed(self):
        name = 'Hitchhikers Guide to the Galaxy'
        self.pat.add_borrowed_book(name)
        self.assertEqual(self.pat.get_borrowed_books(), [name.lower()])

        # Check to make sure the book is not added again
        self.pat.add_borrowed_book(name)
        self.assertEqual(self.pat.get_borrowed_books(), [name.lower()])

    def test_return_borrowed_book(self):
        name = 'Hitchhikers Guide to the Galaxy'
        self.pat.add_borrowed_book(name)
        self.assertEqual(self.pat.get_borrowed_books(), [name.lower()])

        self.pat.return_borrowed_book(name)
        self.assertEqual(self.pat.get_borrowed_books(), [])

    def test_get_fname(self):
        self.assertEqual(self.pat.get_fname(), 'fname')

    def test_get_lname(self):
        self.assertEqual(self.pat.get_lname(), 'lname')

    def test_get_age(self):
        self.assertEqual(self.pat.get_age(), '20')

    def test_get_phone(self):
        self.assertEqual(self.pat.get_memberID(), '1234')

    def test_equals(self):
        pat = patron.Patron('fname', 'lname', '20', '1234')
        self.assertTrue(self.pat == pat)

    def test_not_equals(self):
        pat = patron.Patron('fname', 'lname', '20', '12345')
        self.assertTrue(self.pat != pat)
