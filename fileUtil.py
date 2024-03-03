import json

from PyPDF2 import PdfReader


def readPdf(path):
    reader = PdfReader(path)

    number_of_pages = len(reader.pages)

    text = ""
    for i in range(number_of_pages):
        page = reader.pages[i]
        text += page.extract_text()

    return text.strip()


def write_datas(datas):
    FILE_PATH = './data.txt'

    with open(FILE_PATH, 'w') as output_file:
            json.dump(datas, output_file, indent=2)
