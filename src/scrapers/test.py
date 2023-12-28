from crawler import *
from scraper import *
import timeit


# Performmace testing all scrapers 
def pref_scrapers():
    AVERAGE_ITERATIONS = 50     # Defines the number of iterations to average the result over

    print(f"Mesuaring avreage runtime over {AVERAGE_ITERATIONS} iterations for all scrapers\n----------------------")
    print("Medical text:\t\t", timeit.timeit(
        'extract_medical_text(soup)',       # The code to test
        'soup = fetch_url("https://www.fass.se/LIF/product?userType=2&nplId=20190822000136&docType=7&scrollPosition=352")',     # Any necessary setup
        number=AVERAGE_ITERATIONS,   # Number of times to run
        globals=globals()   # Imports all global symbols in the current scope
        ) / AVERAGE_ITERATIONS
    )
    print("Fass text:\t\t", timeit.timeit(
        'extract_fass_text(soup)',       # The code to test
        'soup = fetch_url("https://www.fass.se/LIF/product?userType=2&nplId=20190822000136&docType=3&scrollPosition=352")',     # Any necessary setup
        number=AVERAGE_ITERATIONS,   # Number of times to run
        globals=globals()   # Imports all global symbols in the current scope
        ) / AVERAGE_ITERATIONS
    )
    print("Product resume:\t\t", timeit.timeit(
        'extract_product_resume(soup)',       # The code to test
        'soup = fetch_url("https://www.fass.se/LIF/product?userType=2&nplId=20190822000136&docType=6&scrollPosition=820")',     # Any necessary setup
        number=AVERAGE_ITERATIONS,   # Number of times to run
        globals=globals()   # Imports all global symbols in the current scope
        ) / AVERAGE_ITERATIONS
    )
    print("Delbarhets info:\t", timeit.timeit(
        'extract_delbarhet(soup)',       # The code to test
        'soup = fetch_url("https://www.fass.se/LIF/product?userType=2&nplId=20190822000136&docType=2000&scrollPosition=820")',     # Any necessary setup
        number=AVERAGE_ITERATIONS,   # Number of times to run
        globals=globals()   # Imports all global symbols in the current scope
        ) / AVERAGE_ITERATIONS
    )
    print("Package info:\t\t", timeit.timeit(
        'extract_package_info(soup)',       # The code to test
        'soup = fetch_url("https://www.fass.se/LIF/product?userType=2&nplId=20190822000136&docType=30&scrollPosition=850")',     # Any necessary setup
        number=AVERAGE_ITERATIONS,   # Number of times to run
        globals=globals()   # Imports all global symbols in the current scope
        ) / AVERAGE_ITERATIONS
    )


def run_tests():
    pass

if __name__ == '__main__':
    pref_scrapers()
