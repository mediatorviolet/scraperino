import shutil
import zipfile


def search_index_from_dict(dict_list, key, value):
    return dict_list.index(next(item for item in dict_list if item[key] == value))


def clean_img_tag(img_tag):
    img_tag["src"] = img_tag["src"].replace('\n', '')

    return img_tag


def rmdir(path_to_dir):
    try:
        shutil.rmtree(path_to_dir)
    except OSError as e:
        print(f"Error: {path_to_dir}: {e.strerror}")


def unzip_all_to_current_directory(zip_file):
    try:
        with zipfile.ZipFile(zip_file) as z:
            z.extractall()
    except OSError as e:
        print(f'Error in sample.utils.unzip_all_to_current_directory: {e.strerror}')


def unzip_all_to_dir(dirname, zip_file):
    try:
        with zipfile.ZipFile(zip_file) as z:
            z.extractall(dirname)
    except OSError as e:
        print(f'Error in sample.utils.unzip_all_to_current_directory: {e.strerror}')