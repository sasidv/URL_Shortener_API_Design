import unittest
from datetime import datetime, timedelta
from flask import Flask
from unittest.mock import MagicMock, patch
from src.server.server import URLShortener  # Adjust import as necessary


class TestURLShortener(unittest.TestCase):
    def setUp(self):
        """Set up the Flask app, client, and mock database instance."""
        self.app = Flask(__name__)
        self.client = self.app.test_client()
        self.app.testing = True

        # Create a mock database instance with default behavior
        self.mock_db_instance = MagicMock()
        self.mock_db_instance.insert_url.return_value = None  # No DB insertion
        self.mock_db_instance.url_exists.return_value = False  # No collision

        # Inject the mock database into the URLShortener
        self.url_shortener = URLShortener(self.app, db=self.mock_db_instance)

    def post_request(self, url):
        return self.client.post('/', json={'url': url})

    def test_shorten_url_success(self):
        response = self.post_request('https://example.com')

        self.assertEqual(response.status_code, 201)
        json_response = response.get_json()
        self.assertIn('short_url', json_response)
        self.assertIn('expires_in', json_response)
        self.assertTrue(len(json_response['short_url']) > 0)

        # Verify `insert_url` was called with correct arguments
        short_url = json_response['short_url'].split('/')[-1]
        self.mock_db_instance.insert_url.assert_called_once_with(
            short_url, 'https://example.com',
            self.mock_db_instance.insert_url.call_args[0][2]
        )

    def test_shorten_url_missing(self):
        """Test the case where no URL is provided."""
        response = self.post_request('')

        self.assertEqual(response.status_code, 400)
        self.mock_db_instance.insert_url.assert_not_called()

    def test_shorten_url_validates_long_url(self):
        """Test the URL validation with a very long URL."""
        long_url = 'https://' + 'a' * 30000 + '.com'
        response = self.post_request(long_url)

        self.assertEqual(response.status_code, 401)
        self.mock_db_instance.insert_url.assert_not_called()

    def test_shorten_url_validates_invalid_url(self):
        """Test the URL validation with an invalid URL."""
        response = self.post_request('invalid')

        self.assertEqual(response.status_code, 402)
        self.mock_db_instance.insert_url.assert_not_called()

    def test_shorten_url_validates_not_allowed_url(self):
        """Test the URL validation for a disallowed URL."""
        not_allowed_url = 'https://facebook.com/gggg'
        response = self.post_request(not_allowed_url)

        self.assertEqual(response.status_code, 403)
        self.mock_db_instance.insert_url.assert_not_called()

    def test_redirect_to_url_valid(self):
        """Test redirection for a valid short URL."""
        # Arrange: Simulate a valid long URL with a future expiration time
        long_url = 'https://example.com'
        self.mock_db_instance.get_url.return_value = (long_url, datetime.now() + timedelta(seconds=100))

        # Act: Send a GET request to the short URL endpoint
        response = self.client.get('/abc123', follow_redirects=False)

        # Assert: Check that the response contains the correct redirection
        self.assertEqual(response.status_code, 302)  # HTTP 302: Redirect
        self.assertEqual(response.headers['Location'], long_url)  # Redirect location matches the long URL
        self.mock_db_instance.get_url.assert_called_once_with('abc123')

if __name__ == '__main__':
    unittest.main()
