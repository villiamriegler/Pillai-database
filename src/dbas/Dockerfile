# Use the official Python image as a base
FROM python:3.10.6

# Set Python to run unbuffered
ENV PYTHONUNBUFFERED 1

# Install Python libraries
RUN pip install psycopg2 requests beautifulsoup4 pdfminer.six

# Copy files
COPY populate_db.py /populate_db.py
COPY products.xml /products.xml

# Run script on start
CMD ["python3", "/populate_db.py"]
