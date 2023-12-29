# Pillai-Database

To get started, download `Docker` on your computer. This allows you to set up 
environments which is exactly the same independent on operating systems etc.

Create a file named `.env` in this folder and enter these variables:
```env
POSTGRES_DB=<mydatabase>
POSTGRES_USER=<myuser>
POSTGRES_PASSWORD=<mypassword>
```

All `<>`-tags can be replaced with your own names and passwords. 

To get start the database run the following command: `docker-compose up -d`. If you want to stop it, run: `docker-compose down`. 

To run the example python code, you need to install psycopg2 by running this in the terminal `python3 -m pip install psycopg2`. Then run the python code with `python3 connect.py`. 
