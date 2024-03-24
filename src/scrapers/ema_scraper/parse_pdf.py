
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTChar, LTTextContainer
import re
import os

leaflets_folder_path = 'ema_leaflets_sv/'
txts_folder_path = 'txt_files/'

def is_empty(text_item):
    text_content = element.get_text().strip()
    return text_content == ""

def is_heading(text_item): # Works for headings! (except Mer information..) Not very generalized...
    text_content = element.get_text().strip()
    return re.search(r"\?$", text_content)


def print_with_lable():
    # Open the file and extract pages
    for page_layout in extract_pages(pdf_file_path):
        for element in page_layout:
            if isinstance(element, LTTextContainer):

                if is_empty(element):
                    print("\tEmpty: ", element.get_text().strip())
                elif is_heading(element):
                    print("\tHeading:", element.get_text().strip())
                else:
                    print("\tText:", element.get_text().strip())


def extract_text(pdf_file_path):
    res = ""
    # Open the file and extract pages
    for page_layout in extract_pages(pdf_file_path):
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                res += element.get_text()
    return res


def create_txt_files(leaflets_folder_path, txts_folder_path):
    for filename in os.listdir(leaflets_folder_path):
        if filename.endswith(".pdf"):
            # Extract text from PDF
            extracted_text = extract_text(leaflets_folder_path + filename)

            # Get filepath for .txt file
            txt_filename = filename[:-4] # removes '.pdf'
            txt_file_path = txts_folder_path + txt_filename + ".txt"

            # Write the extracted text into .txt file
            with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(extracted_text)


def main():
    create_txt_files(leaflets_folder_path, txts_folder_path)

if __name__ == '__main__':
    main()


# Anteckningar:
# Kanske göra en funktion som tar bort "Sida 2/3"
# Kanske göra en funktion som tar bort "EMA/2747/29839"


