import requests
from bs4 import BeautifulSoup

url = "https://github.com/search?q=python&type=repositories"

response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

repo_list = soup.find_all("li", {"class": "repo-list-item"})

for repo in repo_list:
    # repo_owner = repo.find("span", {"class": "mr-2"}).text.strip()

    repo_name = repo.find("a", {"class": "v-align-middle"}).text.strip()

    repo_about = repo.find("p", {"class": "mb-1"}).text.strip()

    repo_keywords = [tag.text.strip() for tag in repo.find_all("a", {"class": "topic-tag-link"})]

    repo_stars = repo.find("a", {"class": "Link--muted"}).text.strip()

    repo_last_updated = repo.find("relative-time").text.strip()

    repo_url = "https://github.com" + repo.find("a", {"class": "v-align-middle"})["href"]


    print("Owner name: ",repo_name.split('/')[0])
    print("Repository Name:", repo_name.split('/')[1])
    print("About:", repo_about)
    print("Keywords:", repo_keywords)
    print("Stars:", repo_stars)
    print("Last Updated:", repo_last_updated)
    print("URL:", repo_url)
    # print("Owner:", repo_owner)
    print()
