
class ErrorMessages:
    URL_REQUIRED = {'error': 'URL is required'}, 400
    URL_TOO_LONG = {'error': 'URL is too long.'}, 401
    INVALID_URL_FORMAT = {'error': 'Invalid URL format.'}, 402
    DOMAIN_NOT_ALLOWED = {'error': 'This domain is not allowed.'}, 403


class Error:
    def __init__(self, error):
        self.error_message = error[0]
        self.error_code = error[1]

