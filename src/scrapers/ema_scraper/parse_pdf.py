

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTChar, LTTextContainer


def is_heading(text_item):
    large_font_size_threshold = 1
    has_large_font = any(isinstance(char, LTChar) and char.size >= large_font_size_threshold for char in text_item)
    return has_large_font

pdf_file_path = 'ema_sv/zydelig-epar-medicine-overview_sv.pdf'

# Open the file and extract pages
for page_layout in extract_pages(pdf_file_path):
    for element in page_layout:
        if isinstance(element, LTTextContainer):
            if is_heading(element):
                print("Heading:", element.get_text().strip())
            else:
                print("Text:", element.get_text().strip())



