import os
import requests


def filedown(url, filename):
    """Write a file from URL
    """
    with open(filename, 'wb') as f_out:
        file = requests.get(url)
        # print(f'writing {filename}')
        f_out.write(file.content)


def main():
    url = input("Paste url: ")
    filename = input("What should we name the file? ")
    filedown(url, filename)
    print(f'File downloaded at {os.path.join(os.getcwd(), filename)}')


if __name__ == "__main__":
    main()
