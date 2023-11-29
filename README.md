# database-412
A placeholder README for the database project for CSE 412.

## Team Members
Danny, Aaron, Neha, Ethan

## Introduction
Here's a placeholder introduction to our project.

## Notes on getting the install to work
Python version requirements: Python 3.8 - Python 3.11

You need psycopg2
`pip3 install psycopg2-binary`

Install streamlit
`pip install streamlit`

I had errors with it, but found this article that fixed the issue:
https://stackoverflow.com/questions/5420789/how-to-install-psycopg2-with-pip-on-python
installed libpq-dev with the correct python version and it was all good

## Setting up the local environment
Make sure that your local database server is running with the following command:
`pg_ctl -D PATH/TO/YOUR/DBSERVERFILE -o '-k /tmp' start`
For students in CSE412, this database server folder is `db412`.

Run the reset_database.sh bash script. This will remove the current 'inventory' database if it exists, then create a new version and populate it with the contents of the dbTables.sql script.