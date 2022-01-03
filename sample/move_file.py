import os
import shutil


def move_file(path, filename, destination_folder):
    shutil.move(os.path.join(path, filename), os.path.join(destination_folder, filename))


def main():
    path = input('Enter folder path: ')
    filename = input('Enter file name: ')
    destination_folder = input('Enter path to destination folder: ')

    move_file(path, filename, destination_folder)


if __name__ == '__main__':
    main()
