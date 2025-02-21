import unittest
from library import ext_api_interface
from unittest.mock import Mock
import requests
import json

class TestExtApiInterface(unittest.TestCase):
    def setUp(self):
        self.api = ext_api_interface.Books_API()
        self.book = "learning python"
        with open('tests_data/ebooks.txt', 'r') as f:
            self.books_data = json.loads(f.read())
        with open('tests_data/json_data.txt', 'r') as f:
            self.json_data = json.loads(f.read())

    def test_make_request_True(self):
        attr = {'json.return_value': dict()}
        requests.get = Mock(return_value = Mock(status_code = 200, **attr))
        self.assertEqual(self.api.make_request(""), dict())

    def test_make_request_connection_error(self):
        ext_api_interface.requests.get = Mock(side_effect=requests.ConnectionError)
        url = "some url"
        self.assertEqual(self.api.make_request(url), None)

    def test_make_request_False(self):
        requests.get = Mock(return_value=Mock(status_code=100))
        self.assertEqual(self.api.make_request(""), None)
    
    

    def test_get_ebooks(self):
        self.api.make_request = Mock(return_value=self.json_data)
        self.assertEqual(self.api.get_ebooks(self.book), self.books_data)

    def test_get_book_info(self):
        info = {'docs': [{'title': 'Learning python'}]}
        self.api.make_request = Mock(return_value=info)
        self.assertEqual(self.api.get_book_info('Learning python'), [{'title': 'Learning python'}])
        
    def test_get_author(self):
        info = {'docs': [{'title': 'Learning python', 'title_suggest': 'jo llama'}], 'title_suggest' : []}
        self.api.make_request = Mock(return_value=info)
        self.assertEqual(self.api.books_by_author('jo llama'), ['jo llama'] )

    def test_availability_none(self):
        info = {}
        self.api.make_request = Mock(return_value=info)
        self.assertEqual(self.api.is_book_available("hello world its me justin wade"), False)

    def test_availability_there(self):
        info = {'docs': [{'title': 'Learning python'}, {'title': "hello world its me justin wade"}]}
        self.api.make_request = Mock(return_value=info)
        self.assertEqual(self.api.is_book_available("hello world its me justin wade"), True)

    def test_get_book_info_not_there(self):
        info = {'docs': []}
        self.api.make_request = Mock(return_value=info)
        self.assertEqual(self.api.get_book_info('hello world'), [])

    def test_get_ebooks_not(self):
        self.api.make_request = Mock(return_value=[])
        self.assertEqual(self.api.get_ebooks(self.book), [])
    
    def test_get_book_info_with_all_fields(self):
        info = {
            'docs': [{
                'title': 'Learning python',
                'publisher': ['Reilly'],
                'publish_year': [2020],
                'language': ['eng']
            }]
        }
        self.api.make_request = Mock(return_value=info)
        expected = [{
            'title': 'Learning python',
            'publisher': ['Reilly'],
            'publish_year': [2020],
            'language': ['eng']
        }]
        self.assertEqual(self.api.get_book_info('Learning python'), expected)
        
    def test_get_ebooks_failed_request(self):
        self.api.make_request = Mock(return_value=None)
        self.assertEqual(self.api.get_ebooks(self.book), [])

    def test_get_ebooks_no_ebooks_available(self):
        info = {'docs': [{'title': 'No Ebook', 'ebook_count_i': 0}]}
        self.api.make_request = Mock(return_value=info)
        self.assertEqual(self.api.get_ebooks(self.book), [])
    
    def test_get_book_info_failed_request(self):
        self.api.make_request = Mock(return_value=None)
        self.assertEqual(self.api.get_book_info('Learning python'), [])

    def test_get_book_info_not_there(self):
        info = {'docs': []}
        self.api.make_request = Mock(return_value=info)
        self.assertEqual(self.api.get_book_info('hello world'), [])

    def test_get_author_empty_results(self):
        info = {'docs': []}
        self.api.make_request = Mock(return_value=info)
        self.assertEqual(self.api.books_by_author('nonexistent author'), [])

    def test_get_author_failed_request(self):
        self.api.make_request = Mock(return_value=None)
        self.assertEqual(self.api.books_by_author('jo llama'), [])
