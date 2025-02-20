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

    def test_add_get_borrowed_books(self):
        self.pat.add_borrowed_book("restitutor")
        self.pat.add_borrowed_book("orbis")
        self.assertEqual(self.pat.get_borrowed_books(), ["restitutor", "orbis"])

    def test_add_borrowed_book_twice(self):
        self.pat.add_borrowed_book("the red and the black")
        self.pat.add_borrowed_book("the red and the black")
        self.assertEqual(self.pat.get_borrowed_books(), ["the red and the black"])

    def test_return_borrowed_book(self):
        self.pat.add_borrowed_book("invictus")
        self.pat.return_borrowed_book("invictus")
        self.assertEqual(self.pat.get_borrowed_books(), [])

    def test_eq(self):
        new_patron = patron.Patron('fname', 'lname', '20', '1234')
        self.assertEqual(self.pat, new_patron)

    def test_ne(self):
        new_patron = patron.Patron('Napoleon', 'Bonaparte', '46', '1815')
        self.assertNotEqual(self.pat, new_patron)
    
    def test_get_fname(self):
        self.assertEqual(self.pat.get_fname(), "fname")

    def test_get_lname(self):
        self.assertEqual(self.pat.get_lname(), "lname")
    
    def test_get_age(self):
        self.assertEqual(self.pat.get_age(), "20")

    def test_get_memberID(self):
        self.assertEqual(self.pat.get_memberID(), "1234")