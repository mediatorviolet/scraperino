import re


def sort_by_name(file_list):
    def atoi(text):
        return int(text) if text.isdigit() else text

    def natural_keys(text):
        return [atoi(c) for c in re.split(r'(\d+)', text)]

    file_list.sort(key=natural_keys)

    return file_list
