# database-412
A placeholder README for the database project for CSE 412.

## Team Members
Danny, Aaron, Neha, Ethan

## Introduction
Here's an introduction to our project, once we found out what it will be.

## Notes on getting the install to work
You need psycopg2
`pip3 install psycopg2`

I had errors with it, but found this article that fixed the issue:
https://stackoverflow.com/questions/5420789/how-to-install-psycopg2-with-pip-on-python
installed libpq-dev with the correct python version and it was all good

## Setting up the local environment

I created a new database called "inventory", this is where the info will be stored locally on my computer. It's hosted on the same server that we made for the class
`createdb inventory`