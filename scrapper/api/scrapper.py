import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Authority": "github.com"
}

# function to get github projects links from query
def generate_query_url(keyword:str,page: int = 1):
    query = ''
    for words in keyword.split(' '):
        query = query + '+' + words
    print(query[1:])
    url = f'https://github.com/search?q={query}&type=repositories&p={page}'
    return url


def get_page_data(url: str):
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content,"html.parser")
        return soup
    else:
        return None

def scrap_projects(soup):

    repo_list = soup.find_all("li", {"class": "repo-list-item"})
    for repo in repo_list:
        # repo_owner = repo.find("span", {"class": "mr-2"}).text.strip()
        try:
            repo_name = repo.find("a", {"class": "v-align-middle"}).text.strip()

            repo_about = repo.find("p", {"class": "mb-1"}).text.strip()

            repo_keywords = [tag.text.strip() for tag in repo.find_all("a", {"class": "topic-tag-link"})]

            repo_stars = repo.find("a", {"class": "Link--muted"}).text.strip()

            repo_last_updated = repo.find("relative-time").text.strip()

            repo_url = "https://github.com" + repo.find("a", {"class": "v-align-middle"})["href"]
        except AttributeError:
            pass
            


