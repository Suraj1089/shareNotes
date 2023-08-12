import requests
from bs4 import BeautifulSoup

# The URL of the GitHub profile
url = 'https://github.com/Suraj1089'

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the element that contains the status
    status_element = soup.find('div', class_='user-status-message-wrapper')

    if status_element:
        status = status_element.find('div').text.strip()
        print(f"Current status: {status}")
    else:
        print("Status element not found")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
