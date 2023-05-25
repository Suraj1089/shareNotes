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
    url = f'https://github.com/search?q={query[1:]}&type=repositories&p={page}'
    return url


def get_page_data(url: str):
    try:
        response = requests.get(url,headers=headers)
    except requests.exceptions.ConnectionError:
        return None
    if response.status_code == 200:
        soup = BeautifulSoup(response.content,"html.parser")
        return soup
    else:
        return None

def scrap_projects(soup):
    result = {'repo_names':[],'repo_about':[],
              'repo_keywords':[],'repo_stars':[],
              'repo_last_updated':[],'repo_url':[],
              'repo_language':[],"viewReadme":[]
              }
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

            button = repo_url + '/blob/master/README.md'
            
            repo_language = repo.find("span", {"itemprop": "programmingLanguage"}).text.strip()  # Extract project language


            result['repo_names'].append(repo_name)
            result['repo_about'].append(repo_about)
            result['repo_keywords'].append(repo_keywords)
            result['repo_stars'].append(repo_stars)
            result['repo_last_updated'].append(repo_last_updated)
            result['repo_url'].append(repo_url)
            result['repo_language'].append(repo_language)
            result['viewReadme'].append(button)

            # print('repo_project_language ',repo_project_language)

        except AttributeError:
            pass
    return result
    

def scrap_readme(url: str):
    readme_data = requests.get(url=url,headers=headers)
    readme = None
    if readme_data.status_code != 404:
        soup = BeautifulSoup(readme_data.content,"html.parser")
        readme = soup.find("article", {"class": "markdown-body entry-content container-lg"})
        return readme
    return None
