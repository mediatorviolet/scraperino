import requests
from bs4 import BeautifulSoup as bs
import csv

URL = "https://voiranime.com/page/"
anime_list = []

for page in range(1, 12):
    req = requests.get(URL + str(page))
    soup = bs(req.text, "html.parser")
    animes = soup.find_all('div', class_='page-item-detail')

    for anime in animes:
        d = {}
        thumbnail = anime.find("img", class_="img-responsive").get('src')
        title = anime.find('div', class_="post-title").find('a').text
        link = anime.find('div', class_="post-title").find('a').get('href')
        score = anime.find('span', class_="score").text

        d["title"] = title
        d["thumbnail"] = thumbnail
        d["score"] = score
        d["link"] = link
        anime_list.append(d)

filename = "anime.csv"
with open(filename, 'w', newline='') as f:
    w = csv.DictWriter(f, ['title', 'thumbnail', 'score', 'link'])
    w.writeheader()
    w.writerows(anime_list)
