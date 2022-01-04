import re
import requests
from bs4 import BeautifulSoup
from sample.custom_sort import sort_by_name


def get_all_chapter_url(base_url):
    req = requests.get(base_url)
    soup = BeautifulSoup(req.text, 'html.parser')

    chapter_url = [url.find('a').get('href') for url in soup.find_all('span', class_='lchx desktop')]

    return sort_by_name(chapter_url)


def get_chapters(base_url):
    urls = get_all_chapter_url(base_url)
    mangas = []
    manga_name = re.search(r"(?<=scan-)(.*)(?=-\d+)", urls[0]).group()
    for url in urls:
        chapter_number = re.search(rf"(?<={manga_name}-)(\d+-\d+|\d+)", url).group()
        mangas.append({"name": manga_name, "url": url, "chapter": chapter_number})
    return mangas


if __name__ == "__main__":
    url = input('paste url: ')
    get_chapters(url)
