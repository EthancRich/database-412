-- You can run an SQL scripts. First log into the database you want to run the script on
-- psql -d inventory

-- once in the database, run the script by using the \i command
-- \i sqlScript.sql

-- You can view all tables in the current database by using a command in the psql shell
-- \dt

-- Now, this was just a testing script. You can just use the following command to get rid the testing table
-- DROP TABLE car;

CREATE TABLE User (
    user_id INT NOT NULL,
    user_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (user_id)
);

CREATE TABLE Project (
    sponsor VARCHAR(255) NOT NULL,
    project_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (sponsor, project_name)
);

CREATE TABLE UserProject (
    user_id INT NOT NULL REFERENCES User(user_id), 
    project_name VARCHAR(255) REFERENCES Project(project_name),
    sponsor VARCHAR(255) REFERENCES Project(sponsor),
    is_team_lead BOOLEAN,
    PRIMARY KEY (user_id, project_name, sponsor)
);

CREATE TABLE Transaction (
    trans_id INT NOT NULL,
    checkout_datetime DATETIME,
    expected_return_datetime DATETIME,
    actual_return_datetime DATETIME,
    comments VARCHAR(1023),
    user_id INT NOT NULL REFERENCES User(user_id)
    PRIMARY KEY (trans_id) 
);