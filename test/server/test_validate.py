import unittest

from src.server.errors import ErrorMessages
from src.server.validate import validate_url_request


class TestValidate(unittest.TestCase):

    def test_validate_url_request_URL_TOO_LONG(self):
        long_url = 'https://' + 'a' * 2049  # Create a URL that is too long
        response = validate_url_request(long_url)
        self.assertEqual(response.error_message, ErrorMessages.URL_TOO_LONG[0])
        self.assertEqual(response.error_code, ErrorMessages.URL_TOO_LONG[1])

    def test_validate_url_request_INVALID_URL_FORMAT(self):
        invalid_url = "invalid_url_format"  # Invalid URL format
        response = validate_url_request(invalid_url)
        self.assertEqual(response.error_message, ErrorMessages.INVALID_URL_FORMAT[0])
        self.assertEqual(response.error_code, ErrorMessages.INVALID_URL_FORMAT[1])

    def test_validate_url_request_DOMAIN_NOT_ALLOWED(self):
        prohibited_url = "https://facebook.com"  # Prohibited domain
        response = validate_url_request(prohibited_url)
        self.assertEqual(response.error_message, ErrorMessages.DOMAIN_NOT_ALLOWED[0])
        self.assertEqual(response.error_code, ErrorMessages.DOMAIN_NOT_ALLOWED[1])

    def test_validate_url_request_VALID_URL(self):
        valid_url = "https://www.valid-url.com"  # Valid URL
        response = validate_url_request(valid_url)
        self.assertTrue(response)  # Should return True for valid URLs

    def test_validate_url_request_EMPTY_URL(self):
        empty_url = ""  # Empty URL
        response = validate_url_request(empty_url)
        self.assertEqual(response.error_message, ErrorMessages.URL_REQUIRED[0])
        self.assertEqual(response.error_code, ErrorMessages.URL_REQUIRED[1])
