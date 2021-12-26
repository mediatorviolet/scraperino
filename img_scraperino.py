import os
import requests
import random
from bs4 import BeautifulSoup

URL = "https://www.deviantart.com/search/deviations?cursor=MTQwYWI2MjA9MyY1OTBhY2FkMD00OCZkMTc0YjZiYz0zZTFkZGFjZTI3NWNmNzM0OTE2M2U2NDk1ZDY3OTdjYg&q=tboi"


def img_scraperino(url, folder):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")

    os.makedirs(os.path.join(os.getcwd(), "loot/" + folder), exist_ok=True)
    os.chdir(os.path.join(os.getcwd(), "loot/" + folder))

    def img_filter(img):
        if '.deviantart' in img['src']:
            return False
        if 'data:image' in img['src']:
            return False
        else:
            return True

    raw_images = soup.find_all('img')
    images = filter(img_filter, raw_images)
    for image in images:
        filename = image['alt'] + str(random.randrange(0, 100, 1)) + '.jpg'
        with open(filename, 'wb') as f:
            im = requests.get(image["src"])
            f.write(im.content)
            print('Writing ' + filename + "...")


img_scraperino(URL, "TBOI")
