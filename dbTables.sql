-- This script creates the tables of our database and inserts a dummy data row for each table.
-- running reset_database.sh will update your local database called 'inventory' by deleting it and remaking it with this script.

-- You can interact with this tables by entering the database with the following command from your CLI:
-- psql -d inventory

CREATE TABLE Users (
    users_id VARCHAR(255) NOT NULL,                        
    users_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (users_id)
);

CREATE TABLE Project (
    project_name VARCHAR(255) NOT NULL,
    sponsor VARCHAR(255) NOT NULL,
    PRIMARY KEY (project_name, sponsor)
);

CREATE TABLE UsersProject (
    users_id VARCHAR(255) NOT NULL, 
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
    users_id VARCHAR(255) NOT NULL REFERENCES Users (users_id),
    equipment_items INT[],                      --array of equip_id's
    checkout_date DATE,
    expected_return_date DATE,
    actual_return_date DATE,
    comments VARCHAR(1023),
    PRIMARY KEY (trans_id) 
);

CREATE TABLE MobileDevice(
    equip_id INT NOT NULL,
    mobile_type VARCHAR(255),
    chipset VARCHAR(255),
    operating_system VARCHAR(255),
    ram VARCHAR(255),          
    storage VARCHAR(255),
    ip_address VARCHAR(45),             --ipv6 is 45 characters and ipv4 is 15 characters
    PRIMARY KEY (equip_id),
    FOREIGN KEY (equip_id) REFERENCES Equipment (equip_id)
);

CREATE TYPE camera_types AS ENUM ('DSLR', 'Mirrorless', 'Point and Shoot', 'Action', '360', 'Drone', 'Other');

CREATE TABLE Camera (
    equip_id INT NOT NULL,
    camera_type camera_types,
    resolution VARCHAR(255),
    megapixels INT,
    sd_card VARCHAR(255),
    PRIMARY KEY (equip_id),
    FOREIGN KEY (equip_id) REFERENCES Equipment(equip_id)
);

CREATE TYPE computer_types AS ENUM ('Desktop', 'Laptop', 'Server', 'Mainframe', 'Other');

CREATE TABLE Computer (
    equip_id INT NOT NULL,
    computer_type computer_types,
    cpu VARCHAR(255),
    gpu VARCHAR(255),
    ram VARCHAR(255),
    storage VARCHAR(255),
    hostname VARCHAR(255),
    operating_system VARCHAR(255),
    local_admin VARCHAR(255),
    ip_address VARCHAR(45),             --ipv6 is 45 characters and ipv4 is 15 characters
    PRIMARY KEY (equip_id),
    FOREIGN KEY (equip_id) REFERENCES Equipment(equip_id)
);

CREATE TYPE board_types AS ENUM ('FPGA', 'Microcontroller', 'Other');

CREATE TABLE FPGADeviceBoard (
    equip_id INT NOT NULL,
    board_type board_types,
    storage VARCHAR(255),
    PRIMARY KEY (equip_id),
    FOREIGN KEY (equip_id) REFERENCES Equipment(equip_id)
);

CREATE TABLE VRARDevice (
    equip_id INT NOT NULL,
    storage VARCHAR(255),
    PRIMARY KEY (equip_id),
    FOREIGN KEY (equip_id) REFERENCES Equipment(equip_id)
);

-- \COPY is a psql command line version, and it has to be formatted like the command all on one line, terminated by new lines and not semicolon.
-- COPY doesn't work here, because COPY reads from the server side, however our CSV files don't exist where the server does (/tmp).
-- This is a better alternative than to require we copy everything to /tmp before using COPY.

\COPY Users FROM 'CSVFiles/Users.csv' DELIMITER ',' CSV HEADER
\COPY Project FROM 'CSVFiles/Project.csv' DELIMITER ',' CSV HEADER
\COPY UsersProject FROM 'CSVFiles/UsersProject.csv' DELIMITER ',' CSV HEADER
\COPY Equipment FROM 'CSVFiles/Equipment.csv' DELIMITER ',' CSV HEADER -- error here
\COPY Transaction FROM 'CSVFiles/Transaction.csv' DELIMITER ',' CSV HEADER
\COPY MobileDevice FROM 'CSVFiles/MobileDevice.csv' DELIMITER ',' CSV HEADER
\COPY Camera FROM 'CSVFiles/Camera.csv' DELIMITER ',' CSV HEADER 
\COPY Computer FROM 'CSVFiles/Computer.csv' DELIMITER ',' CSV HEADER
\COPY FPGADeviceBoard FROM 'CSVFiles/FPGADeviceBoard.csv' DELIMITER ',' CSV HEADER
\COPY VRARDevice FROM 'CSVFiles/VRARDevice.csv' DELIMITER ',' CSV HEADER
