-- You can run an SQL scripts. First log into the database you want to run the script on
-- psql -d inventory

-- once in the database, run the script by using the \i command
-- \i sqlScript.sql

-- You can view all tables in the current database by using a command in the psql shell
-- \dt

-- Now, this was just a testing script. You can just use the following command to get rid the testing table
-- DROP TABLE car;

CREATE TABLE car (
    brand VARCHAR(255)
);