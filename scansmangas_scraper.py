import os
import re
import time
import shutil
import requests
from bs4 import BeautifulSoup
from sample.move_file import move_file
from sample.image_to_pdf import image_to_pdf
from sample.loading_animation import load_bar
from sample.get_chapters import get_chapters
from sample.dict_utils import search_index


# Todo: sur le long terme (ou pas), modulariser le programme pour pouvoir l'utiliser sur d'autres sites


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
        time.sleep(0.1)
        load_bar(i, int(page_nb), prefix="Progress", suffix="Done", length=int(page_nb))
        page = get_page(url + str(i))
        img_tag = page.find_all('img')[1]
        cleaned_img = clean_img_tag(img_tag)
        scans_list.append(cleaned_img)
        time.sleep(0.5)

    return scans_list


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
            os.chdir(dir_name)
        # Todo: Gérer si l'input du directory est pas valide
    else:
        os.makedirs(dir_name)
        os.chdir(dir_name)


def scan_down(scans):
    """Download all scans from list

    :param scans: list
    :return: void
    """
    for i, scan in enumerate(scans):
        filename = re.search(r"(?<=Scan )(.*)", scan['alt']).group(1).replace(' ', '-') + '.jpg'
        with open(filename, 'wb') as f_out:
            time.sleep(0.1)
            load_bar(i + 1, len(scans), prefix=f"Downloading {filename}", suffix='Done', length=len(scans))
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


def increment_url(url, i):
    return clean_base_url(re.sub(r'(?<=-)(\d+)(?=-vf)', str(i), url))


def main():
    print('Program started')
    init_msg = 'Valid URL example:\n' \
               '- https://scansmangas.xyz/manga/solo-leveling-vf-lel-fr-lire-va-scans/\n' \
               '- https://scansmangas.xyz/manga/shingeki-no-kyojin-vf/\n' \
               '- https://scansmangas.xyz/manga/one-piece-vf-lel/\n'
    print(init_msg)

    url = input('Paste url: ')
    folder_destination_path = input('Paste path to destination folder: ')
    first_chapter = input('Enter first chapter number: ')
    last_chapter = input('Enter last chapter number: ')
    print('\n')

    chapters = get_chapters(url)
    start_index = search_index(chapters, 'chapter', first_chapter)
    end_index = search_index(chapters, 'chapter', last_chapter)

    for chap in chapters[start_index:end_index + 1]:
        print(clean_base_url(chap["url"]))
        print('Getting first page...')
        first_page = get_page(clean_base_url(chap["url"]))

        print('Getting page number...')
        page_nb = get_page_nb(first_page)

        print('Creating scans list...')
        scans = get_scans_from_all_pages(page_nb, clean_base_url(chap["url"]))

        print('Setting up directory...')
        dir_name = f"{chap['name']}-{chap['chapter']}"
        set_working_dir(dir_name)

        print('Downloading scans...')
        scan_down(scans)

        print('Creating pdf...')
        image_to_pdf('./', f'{dir_name}.pdf')

        print(f'Moving pdf file to destination folder: {folder_destination_path}')
        move_file(os.getcwd(), dir_name + '.pdf', folder_destination_path)

        print(f'Files downloaded at: {folder_destination_path}')
        os.chdir('..')
        os.chdir('..')

        try:
            shutil.rmtree(f'loot/{dir_name}')
        except OSError as e:
            print("Error: %s: %s" % (f'loot/{dir_name}', e.strerror))


if __name__ == "__main__":
    main()
