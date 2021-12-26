import os
import re
import time
import requests
from bs4 import BeautifulSoup


# Todo: Après le dl, faire function pour grouper les jpg. Si oui, on peut choisir le format (d'abord .pdf)
# Todo: lier le script avec google drive pour envoyer le fichier sur le drive et pouvoir le récup sur phone
# Todo: sur le long terme (ou pas), modulariser le programme pour pouvoir l'utiliser sur d'autres sites
# Todo: print un message au start


def get_page(url, i=''):
    """Get html page from url

    :param url: str
    :param i: str

    :return soup: bytes
    """

    req = requests.get(url + i)
    soup = BeautifulSoup(req.text, 'html.parser')

    return soup


def get_page_nb(first_page):
    """Get the total number of page from the first page

    :param first_page:

    :return: page_nb: str
    """

    nav = first_page.find('div', class_='nav_apb')
    page_list = nav.find_all('a')
    page_nb = page_list[len(page_list) - 2].text

    return page_nb


def get_scans_from_all_pages(page_nb, url):
    """Create a list of all scans from all the pages

    :param page_nb: str
    :param url: str
    :return: scan_list: list
    """
    scans_list = []
    for i in range(1, int(page_nb) + 1):
        page = get_page(url + str(i))
        img_tag = page.find_all('img')[1]
        cleaned_img = clean_img_tag(img_tag)
        scans_list.append(cleaned_img)
        time.sleep(1)

    return scans_list


def get_dir_name(url):
    """Get directory name from html page

    :param url: str
    :return: name: str
    """
    name = re.search(r"(?<=/scan-)(.*)(?=/)", url).group(1)

    return name


def set_working_dir(name):
    """Create new directory and cd into it

    :param name: str
    :return: void
    """
    dir_name = os.path.join(os.getcwd(), 'loot/' + name)

    if os.path.exists(dir_name):
        # Todo: faire une sorte de select
        should_change_name = input(
            f'The directory \'{dir_name}\' already exists.\n Would you like to create a new one? (yes, no) ')

        if should_change_name == 'yes':
            new_name = input('Please enter a new name and press enter: ')
            new_dir_name = os.path.join(os.getcwd(), 'loot/' + new_name)
            os.makedirs(new_dir_name)
            os.chdir(new_dir_name)
        elif should_change_name == 'no':
            os.chdir(os.path.join(dir_name))
        # Todo: Gérer si l'input du directory est pas valide
    else:
        os.makedirs(dir_name)
        os.chdir(os.path.join(dir_name))


def scan_down(scans):
    """Download all scans from list

    :param scans: list
    :return: void
    """
    for scan in scans:
        filename = re.search(r"(?<=Scan )(.*)", scan['alt']).group(1).replace(' ', '-') + '.jpg'
        with open(filename, 'wb') as f_out:
            print('-' * 30)
            print(scan['src'])
            print(f'Downloading {filename}...')
            print('\n')
            sc = requests.get(scan['src'])
            f_out.write(sc.content)


def clean_img_tag(img):
    img["src"] = img["src"].replace('\n', '')

    return img


def clean_base_url(url):
    if url.endswith('?im='):
        return url
    elif url.endswith('/'):
        return url + '?im='
    else:
        trailing_digits = re.search(r"(\d+)$", url).group()

        return url.replace(trailing_digits, '')


def main():
    print('Program started')

    url = clean_base_url(input('Paste url: '))

    print('Getting first page...')
    first_page = get_page(url)

    print('Getting page number...')
    page_nb = get_page_nb(first_page)

    print('Creating scans list...')
    scans = get_scans_from_all_pages(page_nb, url)

    print('Setting up directory...')
    dir_name = get_dir_name(url)
    set_working_dir(dir_name)

    print('Downloading scans...')
    scan_down(scans)

    print(f'Files downloaded at: {os.getcwd()}')


if __name__ == "__main__":
    main()
