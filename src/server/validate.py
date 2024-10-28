from typing import Union
from urllib.parse import urlparse

import validators

from src.server.errors import Error
from src.server.errors import ErrorMessages

prohibited_domains = ['facebook.com', 'malicious.com']


def is_valid_url(url: str) -> bool:
    """
    Validate the given URL.

    Parameters:
    url (str): The URL to validate.

    Returns:
    bool: True if the URL is valid, False otherwise.
    """
    # Check if the URL format is valid
    print(url,"url")
    if not validators.url(url):
        return False

    # Parse the URL to ensure it has a scheme
    parsed_url = urlparse(url)

    # Check if scheme and netloc are present
    if not all([parsed_url.scheme, parsed_url.netloc]):
        return False
    return True


def is_valid_length(url):
    return len(url) < 2048


def validate_url_request(url: str) -> Union[bool, Error]:
    if not url:
        return Error(ErrorMessages.URL_REQUIRED)

    if not is_valid_length(url):
        return Error(ErrorMessages.URL_TOO_LONG)

    if not is_valid_url(url):
        return Error(ErrorMessages.INVALID_URL_FORMAT)

    # Check for prohibited domains
    parsed_url = urlparse(url)

    if parsed_url.netloc in prohibited_domains:
        return Error(ErrorMessages.DOMAIN_NOT_ALLOWED)

    return True
