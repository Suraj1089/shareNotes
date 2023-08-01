import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Authority": "https://github.com/"
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
    except requests.exceptions.ConnectionError as e:
        return None
    if response.status_code == 200:
        soup = BeautifulSoup(response.content,"html.parser")
        return soup
    else:
        return None
    

def scrape_languages(url):
    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    # Find the element containing the language statistics
    bordergrid_div = soup.find_all('div', class_='BorderGrid-cell')
    languages = []

    l = bordergrid_div[-1].find_all('span', class_='color-fg-default text-bold mr-1')
    for i in l:
        languages.append(i.text.strip())

    return ', '.join(languages)




def scrap_projects(soup):
    result = {'Repository':[],'About':[],
              'Keywords':[],'Stars':[],
              'Last Updated':[],'Url':[],
              'Programing Language':[],"Readme":[]
              }
    # class="Box-sc-g0xbh4-0 bItZsX"
    repo_list = soup.find_all("div", {"class": "results-list"})
    print('list ', repo_list)
    for repo in repo_list:
        # repo_owner = repo.find("span", {"class": "mr-2"}).text.strip()
        try:
            # class="Text-sc-17v1xeu-0 qaOIC search-match"
            repo_name = repo.find("a", {"class": "Text-sc-17v1xeu-0 qaOIC search-match"}).text.strip()

            repo_about = repo.find("p", {"class": "mb-1"}).text.strip()

            repo_keywords =','.join([tag.text.strip() for tag in repo.find_all("a", {"class": "topic-tag-link"})])

            repo_stars = repo.find("a", {"class": "Link--muted"}).text.strip()

            repo_last_updated = repo.find("relative-time").text.strip()

            
            repo_url = "https://github.com" + repo.find("a", {"class": "v-align-middle"})["href"]
            button = repo_url + '/blob/master/README.md'
            repo_language = scrape_languages(repo_url) # Extract project language


            result['Repository'].append(repo_name)
            # result['About'].append(repo_about)
            # result['Keywords'].append(repo_keywords)
            # result['Stars'].append(repo_stars)
            # result['Last Updated'].append(repo_last_updated)
            # result['Url'].append(repo_url)
            # result['Programing Language'].append(repo_language)
            # result['Readme'].append(button)


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


def get_github_profile_info(username,headers):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
        profile_data = response.json()
        profile_info = {
            'username': profile_data['login'],
            'name': profile_data['name'],
            'email': profile_data['email'],
            'photo': profile_data['avatar_url'],
            'about': profile_data['bio'],
            'location': profile_data['location'],
            'public_repos': profile_data['public_repos'],
            'followers': profile_data['followers'],
            'following': profile_data['following'],
            'blog': profile_data['blog'],
            'twitter': profile_data['twitter_username'],
            'company': profile_data['company']
        }
        return profile_info
    else:
        return None
