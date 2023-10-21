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

-- Replace all below with downloaded data in this branch
-- Another example I saw if this one doesnt work: COPY persons(first_name, last_name, dob, email) FROM 'C:\sampledb\persons.csv' DELIMITER ',' CSV HEADER;
-- Path will have to change for each person

COPY Users(users_id, users_name)
    FROM '/Users/michaelantar/Desktop/School/CSE412/DB CSV FILES/Data for Database - Users.csv'
    WITH (FORMAT csv);

COPY Project(project_name, sponsor)
    FROM '/Users/michaelantar/Desktop/School/CSE412/DB CSV FILES/Data for Database - Project.csv'
    WITH (FORMAT csv);

COPY UsersProject(users_id, project_name, sponsor, is_team_lead)
    FROM '/Users/michaelantar/Desktop/School/CSE412/DB CSV FILES/Data for Database - UsersProject.csv'
    WITH (FORMAT csv);

COPY Equipment(equip_id, serial_number, product_name, manufacturer, label, category, purchase_date, comments, status, condition)
    FROM '/Users/michaelantar/Desktop/School/CSE412/DB CSV FILES/Data for Database - Equipment.csv'
    WITH (FORMAT csv);

COPY Transaction(trans_id, users_id, expected_return_date, actual_return_date, comments, equipment_items)
    FROM '/Users/michaelantar/Desktop/School/CSE412/DB CSV FILES/Data for Database - Transaction.csv'
    WITH (FORMAT csv);

COPY MobileDevice(equip_id, mobile_type, operating_system, ram, storage, ip_address)
    FROM '/Users/michaelantar/Desktop/School/CSE412/DB CSV FILES/Data for Database - MobileDevice.csv'
    WITH (FORMAT csv);

COPY Camera(equip_id, camera_type, resolution, megapixels, sd_card)
    FROM '/Users/michaelantar/Desktop/School/CSE412/DB CSV FILES/Data for Database - Camera.csv'
    WITH (FORMAT csv);

COPY Computer(equip_id, computer_type, cpu, gpu, ram, storage, hostname, operating_system, local_admin, ip_address)
    FROM '/Users/michaelantar/Desktop/School/CSE412/DB CSV FILES/Data for Database - Computer.csv'
    WITH (FORMAT csv);

COPY FPGADeviceBoard(equip_id, board_type, storage)
    FROM '/Users/michaelantar/Desktop/School/CSE412/DB CSV FILES/Data for Database - FPGADeviceBoard.csv'
    WITH (FORMAT csv);

COPY VRARDevice(equip_id, storage)
    FROM '/Users/michaelantar/Desktop/School/CSE412/DB CSV FILES/Data for Database - VRARDevice.csv'
    WITH (FORMAT csv);
