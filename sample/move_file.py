import os
import re
import shutil


def move_file(path, filename, destination_folder):
    shutil.move(os.path.join(path, filename), os.path.join(destination_folder, filename))


def move_file_full_path(full_path_file, destination_folder):
    dest_file = destination_folder + re.search(r"([^/]+$)", full_path_file).group()
    shutil.move(full_path_file, dest_file)
    return dest_file


def main():
    path = input('Enter folder path: ')
    filename = input('Enter file name: ')
    destination_folder = input('Enter path to destination folder: ')

    move_file(path, filename, destination_folder)


if __name__ == '__main__':
    main()
