import os
from fpdf import FPDF
from PIL import Image
from custom_sort import sort_by_name


def jpg_to_pdf(dirname, filename):
    dpi = 96  # Note for calcs below: 'pt' units are 1/72th of an inch
    pdf = FPDF(unit='pt')
    pdf.set_auto_page_break(0)

    jpg_list = [x for x in sorted(os.listdir(dirname)) if x.endswith('.jpg')]
    jpg_list = sort_by_name(jpg_list)
    # print(jpg_list)

    # Todo: handle landscape format if w > h
    for jpg in jpg_list:
        path = os.path.join(dirname, jpg)
        img = Image.open(path)
        pdf.add_page()
        pdf.image(path, 0, 0, w=img.size[0] / dpi * 72, h=img.size[1] / dpi * 72)

    pdf.output(os.path.join(dirname, filename))


def main():
    dirname = input('dirname: ')
    filename = input('filename: ')

    jpg_to_pdf(dirname, filename)


if __name__ == '__main__':
    main()
