-- You can run an SQL scripts. First log into the database you want to run the script on
-- psql -d inventory

-- once in the database, run the script by using the \i command
-- \i dbTables.sql

-- You can view all tables in the current database by using a command in the psql shell
-- \dt

CREATE TABLE "user" (
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
    user_id INT NOT NULL, 
    project_name VARCHAR(255) NOT NULL,
    sponsor VARCHAR(255) NOT NULL,
    is_team_lead BOOLEAN,
    PRIMARY KEY (user_id, project_name, sponsor),
    FOREIGN KEY (user_id) REFERENCES "user" (user_id),
    FOREIGN KEY (project_name, sponsor) REFERENCES Project (project_name, sponsor)
);

CREATE TABLE Equipment (
    equip_id INT NOT NULL,
    serial_number VARCHAR(255),
    product_name VARCHAR(255),
    manufacturer VARCHAR(255),
    label VARCHAR(255),                         --what does the label mean
    category VARCHAR(255),                      --do we want to abstract this to an int that represents each category? What are the categories
    purchase_date DATE,
    comments VARCHAR(1023),
    "status" VARCHAR(1023),                     --What pre-defined statuses do we want
    condition VARCHAR(255),                     --What pre-defined conditions do we want
    PRIMARY KEY (equip_id)
);

CREATE TABLE Transaction (
    trans_id INT NOT NULL,
    checkout_date DATE,
    expected_return_date DATE,
    actual_return_date DATE,
    comments VARCHAR(1023),
    equipment_items INT[],                      --array of equip_id's
    user_id INT NOT NULL REFERENCES "user" (user_id),
    PRIMARY KEY (trans_id) 
);