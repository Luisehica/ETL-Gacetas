from ntpath import join
from PyPDF2 import PdfFileReader
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import os

import logging
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

def extract_first_page(gaceta, image_output, text_output):

    logging.info("Get first image from pdf")
    images_from_path = convert_from_path('gacetas/'+gaceta, output_file="image_pdf.jpeg")

    image = images_from_path[0]
    fname = 'image/'+ image_output
    image.save(fname,'PNG')
    logging.info("Get text from first page")
    text = pytesseract.image_to_string(Image.open('image/'+image_output))
    with open('text/'+text_output, 'w') as output:
        output.write(text)

def extract_number_pages(pdf_path):
    with open(pdf_path, 'rb') as f:
        pdf = PdfFileReader(f)
        number_of_pages = pdf.getNumPages()
    
    return number_of_pages

if __name__=='__main__':
    gaceta_list = os.listdir('gacetas')
    gaceta_first_page = os.listdir('image')

    gaceta_corrected = []
    for gaceta in gaceta_first_page:
        split_gaceta = gaceta.split("_")
        join_gaceta = split_gaceta[0]+"_"+split_gaceta[1]
        gaceta_corrected.append(join_gaceta)

    gaceta_restante = set(gaceta_list).difference(set(gaceta_corrected))
    print(len(gaceta_list))
    print(len(gaceta_first_page))
    print(len(gaceta_restante))


    for gaceta in gaceta_restante:
        logging.info("Starting getting first page of "+gaceta)
        image_output = gaceta+'_first_page.png'
        text_output = gaceta+'first_page.txt'
        extract_first_page(gaceta, image_output, text_output)
        logging.info("Finishing text extraction")
