-- This script creates the tables of our database and inserts a dummy data row for each table.
-- running reset_database.sh will update your local database called 'inventory' by deleting it and remaking it with this script.

-- You can interact with this tables by entering the database with the following command from your CLI:
-- psql -d inventory

CREATE TABLE Users (
    users_id INT NOT NULL,                        -- ASURITE? or just an internal id? neha: asurite
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

CREATE TABLE MobileDevice(
    equip_id INT NOT NULL,
    type VARCHAR(255),
    chipset VARCHAR(255),
    operating_system VARCHAR(255),
    ram VARCHAR(255),          --should this be an int? or should we let them specify the units?
    storage VARCHAR(255),      --should this be an int? or should we let them specify the units?
    PRIMARY KEY (equip_id),
    FOREIGN KEY (equip_id) REFERENCES Equipment (equip_id)
);

CREATE TABLE Camera (
    equip_id INT NOT NULL,
    type ENUM('DSLR', 'Mirrorless', 'Point and Shoot', 'Action', '360', 'Drone', 'Other'),
    resolution VARCHAR(255),
    megapixels INT,
    sd_card VARCHAR(255),
    PRIMARY KEY (equip_id),
    FOREIGN KEY (equip_id) REFERENCES Equipment(equip_id)
);

CREATE TABLE Computer (
    equip_id INT NOT NULL,
    type ENUM('Desktop', 'Laptop', 'Server', 'Mainframe', 'Other'),
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

CREATE TABLE FPGADeviceBoard (
    equip_id INT NOT NULL,
    type ENUM('FPGA', 'Microcontroller', 'Other'),
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

CREATE TABLE MISC (
    equip_id INT NOT NULL,
    PRIMARY KEY (equip_id),
    FOREIGN KEY (equip_id) REFERENCES Equipment(equip_id)
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

INSERT INTO MobileDevice (equip_id, type, chipset, operating_system, ram, storage, ip_address)
VALUES (1234, 'Smartphone', 'ChipA', 'OS A', '8GB', '128GB', '192.168.1.1');

INSERT INTO Camera (equip_id, type, resolution, megapixels, sd_card)
VALUES (2456, 'DSLR', '4K', 20, '32GB');

INSERT INTO FPGADeviceBoard (equip_id, type, storage)
VALUES (4563, 'TypeA', '16GB');

INSERT INTO VRARDevice (equip_id, storage)
VALUES (5241, '128GB');

INSERT INTO MISC (equip_id, description) --is this right!?
VALUES (6244);

INSERT INTO Computer (equip_id, Type, CPU, GPU, RAM, Storage, Operating_System, Hostname, IP_Address, Local_Admin) 
VALUES (3333, 'Laptop', 'Intel i7-11800H', 'NVIDIA RTX 3050 Ti', '32GB', '1TB SSD', 'Windows 11', 'DELL-XPS-USER', '192.168.1.11', 'admin');

