from hashlib import sha256
from collections import OrderedDict
from flask import Flask, request, redirect, jsonify
from datetime import datetime, timedelta

from src.server import validate
from src.server.errors import ErrorMessages
from src.server.db_operations import Database


class URLShortener:
    def __init__(self, app: Flask, db=None, cache_size=1000):
        self.app = app
        self.db = db or Database()  # Use the provided database instance or create one
        self.expiration_time_in_seconds = 3600  # 1 hour expiration for demo purposes
        self.cache = OrderedDict()
        self.cache_size = cache_size
        self.setup_routes()

    def setup_routes(self):
        self.app.add_url_rule('/', 'shorten_url', self.shorten_url, methods=['POST'])
        self.app.add_url_rule('/<short_url>', 'redirect_to_url', self.redirect_to_url, methods=['GET'])

    def generate_hash(self, long_url: str, counter: int = 0) -> str:
        hash_object = sha256(f"{long_url}{counter}".encode())  # generate a unique hash based on url and the counter
        return hash_object.hexdigest()[:6]


    def shorten_url(self):
        data = request.get_json()
        long_url = data.get('url')

        if not long_url:
            return jsonify(ErrorMessages.URL_REQUIRED[0]), ErrorMessages.URL_REQUIRED[1]

        validation_response = validate.validate_url_request(long_url)
        if validation_response is not True:
            print("Validation_Response: ", validation_response.error_message)
            return jsonify(validation_response.error_message), validation_response.error_code

        counter = 0
        short_url = self.generate_hash(long_url, counter)

        # Check for collisions
        while self.db.url_exists(short_url):
            counter += 1
            short_url = self.generate_hash(long_url, counter)

        expiration_time = datetime.now() + timedelta(seconds=self.expiration_time_in_seconds)

        # Insert the URL into the database
        self.db.insert_url(short_url, long_url, expiration_time)

        return jsonify({
            'short_url': f'http://localhost:5000/{short_url}',
            'expires_in': self.expiration_time_in_seconds
        }), 201

    def redirect_to_url(self, short_url):
        """Redirect to the original URL, using the cache if available."""
        # Check if the short URL is in the cache
        if short_url in self.cache:
            long_url, expiration_time = self.cache[short_url]
            print(f"Cache hit for {short_url}")
        else:
            # If not in cache, fetch from the database
            print(f"Cache miss for {short_url}")
            url_data = self.db.get_url(short_url)
            if not url_data:
                return jsonify({'error': 'Short URL not found'}), 404

            long_url, expiration_time = url_data

            self._add_to_cache(short_url, (long_url, expiration_time))

        if datetime.now() > expiration_time:
            return jsonify({'error': 'URL has expired'}), 410

        return redirect(long_url, code=302)

    def _add_to_cache(self, key, value):
        """Add a new entry to the cache, evicting the oldest if necessary."""
        if key in self.cache:
            # Move the existing entry to the end to mark it as recently used
            self.cache.move_to_end(key)
        self.cache[key] = value

        # If the cache size exceeds the limit, remove the oldest entry
        if len(self.cache) > self.cache_size:
            oldest_key = next(iter(self.cache))
            print(f"Evicting {oldest_key} from cache")
            self.cache.pop(oldest_key)

if __name__ == '__main__':
    app = Flask(__name__)
    url_shortener = URLShortener(app)
    app.run(debug=True)
