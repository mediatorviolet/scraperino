import os
import requests


def filedown(url, filename):
    with open(filename, 'wb') as f_out:
        file = requests.get(url)
        f_out.write(file.content)


def main():
    url = input("Paste url: ")
    filename = input("What should we name the file? ")
    filedown(url, filename)
    # Todo: rendre le lien clickable
    print(f'File downloaded at {os.path.join(os.getcwd(), filename)}')


if __name__ == "__main__":
    main()
