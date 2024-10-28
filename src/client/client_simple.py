import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def post_request(host, long_url):
    # Create a shortened URL
    post_response = requests.post(host, json={'url': long_url}, verify=False)
    short_url = post_response.json().get('short_url')
    if not short_url:
        print(f"# Shortened URL request: error!\n")
    else:
        print(f"# Shortened URL requested for {long_url}: {short_url}\n")
    return short_url


def get_request(short_url):
    # Access the shortened URL, simulating the GET request to follow the redirect
    if short_url:
        get_response = requests.get(short_url, allow_redirects=True, verify=False)
        print(f"# Original URL after redirect: {get_response.url}")
        print(f"Status Code: {get_response.status_code}\n")
        # print(f"Page Content: {get_response.text[:100]}")
    else:
        print(f"# Original URL after redirect: None\n")


if __name__ == "__main__":
    # This script send sample post and get requests to the URL shortner API and receives output

    # 1. Request short URL for 'https://example.com'. Expected output - successful short link generation
    print("Test 1: Request short URL for 'https://example.com'")
    post_request1 = post_request('http://localhost:5000/', 'https://example.com')

    # 2. Get the original URL from the short URL created in step 1. Expected output - 'https://example.com'
    print("Test 2: Get the original URL from the short URL created in step 1.")
    get_request(post_request1)

    # 3. Request short URL for 'https://en.wikipedia.org/wiki/Flask_(web_framework)'. Expected output - successful short link generation.
    print("Test 3: Request short URL for 'https://en.wikipedia.org/wiki/Flask_(web_framework)'.")
    post_request2 = post_request('http://localhost:5000/', 'https://en.wikipedia.org/wiki/Flask_(web_framework)')

    # 4. Request short URL for 'https://www.techtarget.com/searchdatamanagement/definition/database'. Expected output - successful short link generation.
    print("Test 4: Request short URL for 'https://www.techtarget.com/searchdatamanagement/definition/database'")
    post_request3 = post_request('http://localhost:5000/','https://www.techtarget.com/searchdatamanagement/definition/database')

    # 5. Get the original URL from the short URL created in step 4 - 'https://www.techtarget.com/searchdatamanagement/definition/database'
    print("Test 5: Get the original URL from the short URL created in step 4")
    get_request(post_request3)

    # 6. Request short URL for 'https://facebook.com' - Expected output - error!, since facebook.com links are not allowed
    print("Test 6: Request short URL for 'https://facebook.com'. Expects an error since the domain is prohibited.")
    post_request4 = post_request('http://localhost:5000/','https://facebook.com')

    # 7. Get the original URL from the short URL created in step 1. Expected output - 'https://example.com'
    print("Test 7: Get the original URL from the short URL created in step 1.")
    get_request(post_request1)

    # 8. Request short URL for 'https://example.com'. Expected output - successful short link generation. This short link will be different from the one in step 1 as we create a unique link for each new URL request.
    print("Test 8: Request short URL for 'https://example.com'. Note that this short link is different from the one in step 1 as we create a unique link for each new URL request.")
    post_request5 = post_request('http://localhost:5000/', 'https://example.com')

    # 9. Request short URL for a very long URL - Expected output - error!. Very long links are not supported by the URL shortner to avoid mallicious inputs.
    print("Test 9: Request short URL for a very long URL. Expects an error since it exceeds the length of the allowed maximum url length.")
    post_request6 = post_request('http://localhost:5000/',f'https://' + 'a' * 3000 + '.com')

    #10. Get the original URL from the short URL created in step 8. Expected output - error!, since the URL was not successfully created in step 8.
    print("Test 10: Get the original URL from the short URL created in step 8. Expects an error since the URL was not successfully generated in step 8")
    get_request(post_request6)
