import os
from fpdf import FPDF
from PIL import Image
from custom_sort import sort_by_name


def jpg_to_pdf(dirname, filename):
    dpi = 96  # Note for calcs below: 'pt' units are 1/72th of an inch
    pdf = FPDF(unit='pt')
    pdf.set_auto_page_break(0)

    jpg_list = [x for x in os.listdir(dirname) if x.endswith('.jpg')]
    sorted_jpg_list = sort_by_name(jpg_list)

    # Todo: handle landscape format if w > h
    # Ça met bien en landscape quand nécessaire mais le format de l'image est fucked...
    for jpg in sorted_jpg_list:
        path = os.path.join(dirname, jpg)
        img = Image.open(path)
        width = img.size[0]
        height = img.size[1]

        if width > height:
            pdf.add_page(orientation='L')
            pdf.image(path, 0, 0, w=width / dpi * 72, h=height / dpi * 72)
        else:
            pdf.add_page(orientation='P')
            pdf.image(path, 0, 0, w=width / dpi * 72, h=height / dpi * 72)

    pdf.output(os.path.join(dirname, filename))


def main():
    dirname = input('Path to directory: ')
    filename = input('Output file name: ')
    if not filename.endswith('.pdf'):
        filename += filename + '.pdf'

    jpg_to_pdf(dirname, filename)


if __name__ == '__main__':
    main()
