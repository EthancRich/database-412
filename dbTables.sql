-- This script creates the tables of our database and inserts a dummy data row for each table.
-- running reset_database.sh will update your local database called 'inventory' by deleting it and remaking it with this script.

-- You can interact with this tables by entering the database with the following command from your CLI:
-- psql -d inventory

CREATE TABLE Users (
    users_id INT NOT NULL,                        -- ASURITE? or just an internal id?
    users_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (users_id)
);

CREATE TABLE Project (
    project_name VARCHAR(255) NOT NULL,
    sponsor VARCHAR(255) NOT NULL,
    PRIMARY KEY (project_name, sponsor)
);

CREATE TABLE UsersProject (
    users_id INT NOT NULL, 
    project_name VARCHAR(255) NOT NULL,
    sponsor VARCHAR(255) NOT NULL,
    is_team_lead BOOLEAN,
    PRIMARY KEY (users_id, project_name, sponsor),
    FOREIGN KEY (users_id) REFERENCES Users (users_id),
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
    users_id INT NOT NULL REFERENCES Users (users_id),
    PRIMARY KEY (trans_id) 
);

INSERT INTO Users (users_id, users_name) 
VALUES (1000, 'Jane Doe');

INSERT INTO Project (project_name, sponsor)
VALUES ('Janes Team', 'State Farm');

INSERT INTO UsersProject (users_id, project_name, sponsor, is_team_lead)
VALUES (1000, 'Janes Team', 'State Farm', TRUE);

INSERT INTO Equipment (equip_id, serial_number, product_name, manufacturer, label, category, purchase_date, comments, "status", condition)
VALUES (8877, 'XY234', 'VR Headset', 'Meta', 'None', 'AR/VR', '2022-11-23', NULL, 'checked out', 'New');

INSERT INTO Transaction (trans_id, checkout_date, expected_return_date, actual_return_date, comments, equipment_items, users_id)
VALUES (1, '2023-03-12', '2023-05-11', NULL, NULL, '{8877}', 1000);