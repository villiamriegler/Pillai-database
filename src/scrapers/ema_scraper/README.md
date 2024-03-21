# Explanation for EMA
The file `parse_csv.py` goes through all valid drugs listed on EMA: https://www.ema.europa.eu/system/files/documents/other/medicines_output_european_public_assessment_reports_en.xlsx. The data was retrieved March 18. For a drug to be considered valid it must be meant for humans and be approved by EMA. 

The file `url_scraper.py` contains methods for finding links to PDF-documents in Swedish and English, as well as a method to download these PDF:s. 

`crawler.py` is used to call url_scraper based on the extracted links from parse_csv. 

`find_pairs.py` finds all documents with matching names but in different languages. These names have been saved to `translations.txt`. These are documents we can use to train a translation model. 

`parse_pdf.py` well extract text from the PDF:s. 

# Order of execution
- 1) Download https://www.ema.europa.eu/system/files/documents/other/medicines_output_european_public_assessment_reports_en.xlsx and convert to a CSV file
- 2) `parse_csv.py`
- 3) `crawler.py`
- 4) `find_pairs.py` (or check `translations.txt`)
- 5) `parse_pdf.py` 