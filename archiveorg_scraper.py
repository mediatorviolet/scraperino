import re
import json
import requests
import sample.utils as utils
from bs4 import BeautifulSoup
from sample.filedown import filedown
from sample.loading_animation import load_bar
from sample.image_to_pdf import image_to_pdf as itp
from sample.move_file import move_file


def only_jp2(href):
    return href and re.compile(r"(jp2\.zip)").search(href) and not href.endswith('/')


def get_links_as_json(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')

    a_tags = soup.find_all(href=only_jp2)
    mangas = [{"url": url + manga.get('href'), "name": manga.text.replace('_jp2.zip', '')} for manga in a_tags]

    json_object = json.dumps(mangas)

    filename = 'loot/' + re.search(r"(?<=download/)(.*[^/])", url).group() + '.json'
    with open(filename, 'w') as f_out:
        f_out.write(json_object)

    return filename


def download_from_json(filename, destination_folder):
    with open(filename, 'r') as f_in:
        data = json.load(f_in)
        for i, manga in enumerate(data[20:20]):
            load_bar(i + 1, len(data), prefix="Progress", suffix="Done", length=len(data))
            zip_file = f"loot/{manga['name']}.zip"
            filedown(manga['url'], zip_file)
            handle_zip_file(zip_file, destination_folder)


def handle_zip_file(file, destination_folder):
    utils.unzip_all_to_dir("loot", file)
    itp(file.replace('.zip', '_jp2'), file.replace('.zip', '.pdf').replace('loot/', ''))
    move_file(file.replace('.zip', '_jp2'), file.replace('.zip', '.pdf').replace('loot/', ''), destination_folder)
    utils.rmdir(file.replace('.zip', '_jp2'))
    # Todo: rm remaining zipfile


def main():
    yes = ['yes', 'y', 'ye']
    no = ['no', 'n']

    should_create_json = input('Do you already have the json file? (no if not sure) ')

    if should_create_json in no:
        print('Valid URL example:\n- https://archive.org/download/{id}')
        url = input('Paste URL: ')
        json_file = get_links_as_json(url)
    else:
        json_file = input('Paste path to json file: ')

    should_dl = input('Do you want to download the files? (yes, no) ')
    if should_dl in yes:
        destination_folder = input('Paste destination folder: ')
        print('Downloading the files')
        download_from_json(json_file, destination_folder)


if __name__ == '__main__':
    main()
