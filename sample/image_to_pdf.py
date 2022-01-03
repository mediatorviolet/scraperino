import os
from PIL import Image
from sample.custom_sort import sort_by_name


def image_to_pdf(dirname, filename):
    image_list = [Image.open(os.path.join(dirname, x)).convert('L') for x in sort_by_name(os.listdir(dirname)) if
                  x.endswith('.jpg')]
    image_list[0].save(dirname + filename, save_all=True, append_images=image_list[1:])


def main():
    dirname = input('Path to directory: ')
    filename = input('Output file name: ')
    if not filename.endswith('.pdf'):
        filename += filename + '.pdf'

    image_to_pdf(dirname, filename)


if __name__ == '__main__':
    main()
