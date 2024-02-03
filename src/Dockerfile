# Use the official Python image as a base
FROM python:3.10.6

# Set Python to run unbuffered
ENV PYTHONUNBUFFERED 1

# Install Python libraries
RUN pip install psycopg2 requests beautifulsoup4 

# Copy files
#COPY scrapers /scrapers/
#COPY dbas /dbas/
COPY test.py /test.py

# Run script on start
CMD ["python3", "/test.py"]
