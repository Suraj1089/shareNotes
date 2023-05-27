import requests
from bs4 import BeautifulSoup
url = "https://github.com/Suraj1089/Heart-Charity"
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')

# Find the element containing the language statistics

bordergrid_div = soup.find_all('div', class_='BorderGrid-cell')
languages = []

l = bordergrid_div[-1].find_all('span', {"class":"color-fg-default text-bold mr-1"})
for i in l:
    languages.append(i.text.strip())

lan_string = ','.join(languages)

return lan_string