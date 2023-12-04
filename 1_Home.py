# CSE 412 Database Management System
# home.py
# Login process - Neha
# Item management - Ethan

import streamlit as st
import psycopg2
import pandas as pd
import sys
import time

#########################################
###---------- INTIALIZATION ----------###
#########################################

# Initialize session state for login status
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['user_role'] = None

# homeview describes the main table being displayed each run.
#   0 - no table to display.    1 - all table
#   2 - out table               3 - in table            4 - hist table
if 'homeview' not in st.session_state:
    st.session_state['homeview'] = 0

# add_edit_remove tells which button menu is currently being used.
#   0 - no button being used.   1 - Add button
#   2 - Edit button             3 - Remove button       4 - more info
if 'add_edit_remove' not in st.session_state:
    st.session_state['add_edit_remove'] = 0

## Write something here

if 'edit_display' not in st.session_state:
    st.session_state['edit_display'] = 0

###########################################
###---------- LOGIN FUNCTIONS ----------###
###########################################

def load_users_from_csv(file_path):
    #Load the CSV file into a pandas dataframe
    df = pd.read_csv(file_path)
    users = {row['users_id']: {"password": "123", "role": "student", "name": row['users_name']} for index, row in df.iterrows()}
    
    # Add a manual entry for the admin user
    users['admin'] = {"password": "adminpass", "role": "admin", "name": "Admin User"}
    return users

users = load_users_from_csv("CSVFiles/Users.csv")

# Function to display centered login form
def show_login_form():
    # Empty space for vertical centering
    for _ in range(10):
        st.write("")

    # Centering the login form horizontally
    col1, col2, col3 = st.columns([1,2,1])
    with col2:  # Middle column
        st.write("## Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        user_type = st.radio("Select your role:", ("Admin", "Student"))
        if st.button("Login"):
            return username, password, user_type
    return None, None, None

# Function to check user credentials
def check_credentials(username, password, user_type):
    user_info = users.get(username)
    if user_info and user_info["password"] == password and user_info["role"] == user_type.lower():
        st.session_state['user_name'] = user_info["name"] #Store the user name in the session state = global variable
        return user_info["role"]
    else:
        st.error("The username or password you entered is incorrect.")
        return None

###---------- DB CONNECTIVITY ----------###

def connect_to_db():
    #Connect to database and close connection on demand
    conn = psycopg2.connect(
        host="bubble.db.elephantsql.com",
        port="5432",
        database="aqqphukw",
        user="aqqphukw",
        password="LhbOXcM_ZWgawdTaxF3r3uxMdJqhyd1H" #THIS IS UNSAFE. REMOVE THIS IN THE FUTURE.
    )
    return conn

def print_psycopg2_exception(err):
    # Function for printing error codes with psycopg2
    # Source: https://kb.objectrocket.com/postgresql/python-error-handling-with-the-psycopg2-postgresql-adapter-645

    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()

    # get the line number when exception occured
    line_num = traceback.tb_lineno

    # print the connect() error
    print ("\npsycopg2 ERROR:", err, "on line number:", line_num)
    print ("psycopg2 traceback:", traceback, "-- type:", err_type)

    # psycopg2 extensions.Diagnostics object attribute
    print ("\nextensions.Diagnostics:", err)

# Actually start up the cursor for the queries
conn = connect_to_db()
cur = conn.cursor()

###---------- DISPLAY FUNCTIONS ----------###

def display_all_table():
    cur.execute("SELECT * FROM Equipment;") #equip_id,serial_number,product_name,manufacturer,label,category,purchase_date,comments,status,condition
    raw_data = cur.fetchall()
    column_names = ['ID#', 'Serial#', 'Name', 'Manufacturer', 'Label', 'Category', 'Purchase Date', 'Comments', 'Status', 'Condition']
    data_frame = pd.DataFrame(raw_data, columns=column_names)
    st.dataframe(data_frame)

def display_out_table():
    cur.execute("""
        SELECT * 
        FROM Equipment
        WHERE status = 'Unavailable';
        """)
    raw_data = cur.fetchall()
    column_names = ['ID#', 'Serial#', 'Name', 'Manufacturer', 'Label', 'Category', 'Purchase Date', 'Comments', 'Status', 'Condition']
    data_frame = pd.DataFrame(raw_data, columns=column_names)
    st.dataframe(data_frame)

def display_in_table():
    cur.execute("""
        SELECT * 
        FROM Equipment
        WHERE status = 'Available';
        """)
    raw_data = cur.fetchall()
    column_names = ['ID#', 'Serial#', 'Name', 'Manufacturer', 'Label', 'Category', 'Purchase Date', 'Comments', 'Status', 'Condition']
    data_frame = pd.DataFrame(raw_data, columns=column_names)
    st.dataframe(data_frame)

def display_hist_table():
    cur.execute("""
        SELECT users_id, equipment_items, checkout_date, expected_return_date, actual_return_date, comments 
        FROM Transaction;
        """)
    raw_data = cur.fetchall()
    column_names = ['ASURITE', 'Equipment IDs', 'Checked Out', 'Return Due', 'Checked In', 'Comments']
    data_frame = pd.DataFrame(raw_data, columns=column_names)
    st.dataframe(data_frame)

def remove_callback(equip_id):
    
    cur.execute(f"""
    SELECT COUNT(*)
    FROM Equipment
    WHERE equip_id = {equip_id};
    """)
    if cur.fetchall()[0][0] == 1:
        try:
            cur.execute(f"""
            DELETE FROM Equipment
            WHERE equip_id = {equip_id};
            """)
            conn.commit()
            st.success("Item sucessfully removed.")
            time.sleep(1)
            st.rerun()
        except Exception as err:
            print_psycopg2_exception(err)
            conn.rollback()
    else:
        st.error("Equip_id invalid. ID must be present and unique.")

def display_remove_items():
    eid = st.number_input('Select the ID# of the item you\'d like to remove:', min_value=1, value=None, step=1)
    if st.button('Confirm') and eid != None:
        remove_callback(eid)

def display_mobile_device_entry():
    col1, col2 = st.columns([1,1])

    serial_selection = col1.text_input('Serial Number', max_chars=255) ###
    product_selection = col1.text_input('Product Name', max_chars=255) ###
    manufacturer_selection = col1.text_input('Manufacturer', max_chars=255) ###
    label_selection = col1.text_input('Label', max_chars=255)
    date_selection = col2.date_input('Purchase Date', format="MM/DD/YYYY", value=None) ###
    comment_selection = col2.text_input('Comments', max_chars=1023)
    status_selection = col2.selectbox('Status', ('Available', 'Unavailable'), index=None, placeholder="Select from dropdown...") ###
    condition_selection = col2.selectbox('Condition', ('Good', 'Issues', 'Broken'), index=None, placeholder="Select from dropdown...") ###

    mobile_type_selection = col1.selectbox('Mobile Type', ('Smartphone', 'Other'), index=None, placeholder="Select from dropdown...") ###
    chipset_selection = col1.text_input('Chipset', max_chars=255)
    os_selection = col1.text_input('Operation System', max_chars=255)
    ram_selection = col2.text_input('RAM', max_chars=255)
    storage_selection = col2.text_input('Storage', max_chars=255)
    ip_selection = col2.text_input('IP Address', max_chars=45)

    if st.button('Submit'):
        if not (serial_selection != "" and product_selection != "" and manufacturer_selection != "" and label_selection != "" and date_selection != None and comment_selection != "" and status_selection != None and condition_selection != None and mobile_type_selection != None and chipset_selection != "" and os_selection != "" and ram_selection != "" and storage_selection != "" and ip_selection != ""):
            st.error("One or more required fields are not filled in.")
        else:
            try:
                cur.execute("SELECT MAX(equip_id) FROM Equipment;")
                maxID = cur.fetchall()[0][0]
                
                cur.execute("""
                INSERT INTO Equipment (equip_id, serial_number, product_name, manufacturer, label, category, purchase_date, comments, \"status\", condition)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, (maxID+1, serial_selection, product_selection, manufacturer_selection, label_selection, "Mobile Devices", date_selection, comment_selection, status_selection, condition_selection))

                cur.execute("""
                INSERT INTO MobileDevice (equip_id,mobile_type,chipset,operating_system,ram,storage,ip_address)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
                """, (maxID+1, mobile_type_selection, chipset_selection, os_selection, ram_selection, storage_selection, ip_selection))

                conn.commit()
                st.success("Item sucessfully added.")
                st.session_state['add_edit_remove'] = 0
                time.sleep(1)
                st.rerun()
            except Exception as err:
                print_psycopg2_exception(err)
                conn.rollback()
            
def display_camera_entry(): # equip_id,camera_type,resolution,megapixels,sd_card

    col1, col2 = st.columns([1,1])

    serial_selection = col1.text_input('Serial Number', max_chars=255) ###
    product_selection = col1.text_input('Product Name', max_chars=255) ###
    manufacturer_selection = col1.text_input('Manufacturer', max_chars=255) ###
    label_selection = col1.text_input('Label', max_chars=255)
    date_selection = col2.date_input('Purchase Date', format="MM/DD/YYYY", value=None) ###
    comment_selection = col2.text_input('Comments', max_chars=1023)
    status_selection = col2.selectbox('Status', ('Available', 'Unavailable'), index=None, placeholder="Select from dropdown...") ###
    condition_selection = col2.selectbox('Condition', ('Good', 'Issues', 'Broken'), index=None, placeholder="Select from dropdown...") ###

    camera_type_selection = col1.selectbox('Camera Type', ('DSLR', 'Mirrorless', 'Point and Shoot', 'Action', '360', 'Drone', 'Other'), index=None, placeholder="Select from dropdown...") ###
    resolution = col1.text_input('Resolution', max_chars=255)
    megapixels = col2.number_input('Megapixels', min_value=1, value=None, step=1)
    sd_card = col2.text_input('SD Storage Size', max_chars=255)

    if st.button('Submit'):
        if not (serial_selection != "" and product_selection != "" and manufacturer_selection != "" and label_selection != "" and date_selection != None and comment_selection != "" and status_selection != None and condition_selection != None and camera_type_selection != None and resolution != "" and megapixels != "" and sd_card != ""):
            st.error("One or more required fields are not filled in.")
        else:
            try:
                cur.execute("SELECT MAX(equip_id) FROM Equipment;")
                maxID = cur.fetchall()[0][0]
                
                cur.execute("""
                INSERT INTO Equipment (equip_id, serial_number, product_name, manufacturer, label, category, purchase_date, comments, \"status\", condition)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, (maxID+1, serial_selection, product_selection, manufacturer_selection, label_selection, "Camera", date_selection, comment_selection, status_selection, condition_selection))

                cur.execute("""
                INSERT INTO Camera (equip_id,camera_type,resolution,megapixels,sd_card)
                VALUES (%s, %s, %s, %s, %s);
                """, (maxID+1, camera_type_selection, resolution, megapixels, sd_card))

                conn.commit()
                st.success("Item sucessfully added.")
                st.session_state['add_edit_remove'] = 0
                time.sleep(1)
                st.rerun()
            except Exception as err:
                print_psycopg2_exception(err)
                conn.rollback()

def display_computer_entry():
    col1, col2 = st.columns([1,1])

    serial_selection = col1.text_input('Serial Number', max_chars=255) ###
    product_selection = col1.text_input('Product Name', max_chars=255) ###
    manufacturer_selection = col1.text_input('Manufacturer', max_chars=255) ###
    label_selection = col1.text_input('Label', max_chars=255)
    date_selection = col2.date_input('Purchase Date', format="MM/DD/YYYY", value=None) ###
    comment_selection = col2.text_input('Comments', max_chars=1023)
    status_selection = col2.selectbox('Status', ('Available', 'Unavailable'), index=None, placeholder="Select from dropdown...") ###
    condition_selection = col2.selectbox('Condition', ('Good', 'Issues', 'Broken'), index=None, placeholder="Select from dropdown...") ###

    computer_type = col1.selectbox('Computer Type', ('Desktop', 'Laptop', 'Server', 'Mainframe', 'Other'), index=None, placeholder="Select from dropdown...") ###
    cpu = col1.text_input('CPU', max_chars=255)
    gpu = col1.text_input('GPU', max_chars=255)
    ram = col1.text_input('RAM', max_chars=255)
    storage = col1.text_input('Storage Size', max_chars=255)
    hostname = col2.text_input('Host Name', max_chars=255)
    os = col2.text_input('Operating System', max_chars=255)
    local_admin = col2.text_input('Local Admin', max_chars=255)
    ip = col2.text_input('IP Address', max_chars=45)

    if st.button('Submit'):
        if not (serial_selection != "" and product_selection != "" and manufacturer_selection != "" and label_selection != "" and date_selection != None and comment_selection != "" and status_selection != None and condition_selection != None and computer_type != None and cpu != "" and gpu != "" and ram != "" and storage != "" and hostname != "" and os != "" and local_admin != "" and ip != ""):
            st.error("One or more required fields are not filled in.")
        else:
            try:
                cur.execute("SELECT MAX(equip_id) FROM Equipment;")
                maxID = cur.fetchall()[0][0]
                
                cur.execute("""
                INSERT INTO Equipment (equip_id, serial_number, product_name, manufacturer, label, category, purchase_date, comments, \"status\", condition)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, (maxID+1, serial_selection, product_selection, manufacturer_selection, label_selection, "Computer", date_selection, comment_selection, status_selection, condition_selection))

                cur.execute("""
                INSERT INTO Computer (equip_id,computer_type,cpu,gpu,ram,storage,hostname,operating_system,local_admin,ip_address)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, (maxID+1, computer_type, cpu, gpu, ram, storage, hostname, os, local_admin, ip))

                conn.commit()
                st.success("Item sucessfully added.")
                st.session_state['add_edit_remove'] = 0
                time.sleep(1)
                st.rerun()
            except Exception as err:
                print_psycopg2_exception(err)
                conn.rollback()

def display_fpga_entry(): # equip_id,board_type,storage
    col1, col2 = st.columns([1,1])

    serial_selection = col1.text_input('Serial Number', max_chars=255) ###
    product_selection = col1.text_input('Product Name', max_chars=255) ###
    manufacturer_selection = col1.text_input('Manufacturer', max_chars=255) ###
    label_selection = col1.text_input('Label', max_chars=255)
    date_selection = col2.date_input('Purchase Date', format="MM/DD/YYYY", value=None) ###
    comment_selection = col2.text_input('Comments', max_chars=1023)
    status_selection = col2.selectbox('Status', ('Available', 'Unavailable'), index=None, placeholder="Select from dropdown...") ###
    condition_selection = col2.selectbox('Condition', ('Good', 'Issues', 'Broken'), index=None, placeholder="Select from dropdown...") ###

    board_type = col1.selectbox('Board Type', ('FPGA', 'Microcontroller', 'Other'), index=None, placeholder="Select from dropdown...") ###
    storage = col2.text_input('Storage Size', max_chars=255)

    if st.button('Submit'):
        if not (serial_selection != "" and product_selection != "" and manufacturer_selection != "" and label_selection != "" and date_selection != None and comment_selection != "" and status_selection != None and condition_selection != None and board_type != None and storage != ""):
            st.error("One or more required fields are not filled in.")
        else:
            try:
                cur.execute("SELECT MAX(equip_id) FROM Equipment;")
                maxID = cur.fetchall()[0][0]
                
                cur.execute("""
                INSERT INTO Equipment (equip_id, serial_number, product_name, manufacturer, label, category, purchase_date, comments, \"status\", condition)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, (maxID+1, serial_selection, product_selection, manufacturer_selection, label_selection, "FPGA Board", date_selection, comment_selection, status_selection, condition_selection))

                cur.execute("""
                INSERT INTO FPGADeviceBoard (equip_id,board_type,storage)
                VALUES (%s, %s, %s);
                """, (maxID+1, board_type, storage))

                conn.commit()
                st.success("Item sucessfully added.")
                st.session_state['add_edit_remove'] = 0
                time.sleep(1)
                st.rerun()
            except Exception as err:
                print_psycopg2_exception(err)
                conn.rollback()

def display_vrar_entry(): # equip_id,storage

    col1, col2 = st.columns([1,1])

    serial_selection = col1.text_input('Serial Number', max_chars=255) ###
    product_selection = col1.text_input('Product Name', max_chars=255) ###
    manufacturer_selection = col1.text_input('Manufacturer', max_chars=255) ###
    label_selection = col1.text_input('Label', max_chars=255)
    date_selection = col2.date_input('Purchase Date', format="MM/DD/YYYY", value=None) ###
    comment_selection = col2.text_input('Comments', max_chars=1023)
    status_selection = col2.selectbox('Status', ('Available', 'Unavailable'), index=None, placeholder="Select from dropdown...") ###
    condition_selection = col2.selectbox('Condition', ('Good', 'Issues', 'Broken'), index=None, placeholder="Select from dropdown...") ###

    storage = col1.text_input('Storage Size', max_chars=255)

    if st.button('Submit'):
        if not (serial_selection != "" and product_selection != "" and manufacturer_selection != "" and label_selection != "" and date_selection != None and comment_selection != "" and status_selection != None and condition_selection != None and storage != ""):
            st.error("One or more required fields are not filled in.")
        else:
            try:
                cur.execute("SELECT MAX(equip_id) FROM Equipment;")
                maxID = cur.fetchall()[0][0]
                
                cur.execute("""
                INSERT INTO Equipment (equip_id, serial_number, product_name, manufacturer, label, category, purchase_date, comments, \"status\", condition)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, (maxID+1, serial_selection, product_selection, manufacturer_selection, label_selection, "VR/AR Device", date_selection, comment_selection, status_selection, condition_selection))

                cur.execute("""
                INSERT INTO VRARDevice (equip_id,storage)
                VALUES (%s, %s);
                """, (maxID+1, storage))

                conn.commit()
                st.success("Item sucessfully added.")
                st.session_state['add_edit_remove'] = 0
                time.sleep(1)
                st.rerun()
            except Exception as err:
                print_psycopg2_exception(err)
                conn.rollback()

def display_other_entry():

    col1, col2 = st.columns([1,1])

    serial_selection = col1.text_input('Serial Number', max_chars=255) ###
    product_selection = col1.text_input('Product Name', max_chars=255) ###
    manufacturer_selection = col1.text_input('Manufacturer', max_chars=255) ###
    label_selection = col1.text_input('Label', max_chars=255)
    date_selection = col2.date_input('Purchase Date', format="MM/DD/YYYY", value=None) ###
    comment_selection = col2.text_input('Comments', max_chars=1023)
    status_selection = col2.selectbox('Status', ('Available', 'Unavailable'), index=None, placeholder="Select from dropdown...") ###
    condition_selection = col2.selectbox('Condition', ('Good', 'Issues', 'Broken'), index=None, placeholder="Select from dropdown...") ###

    if st.button('Submit'):
        if not (serial_selection != "" and product_selection != "" and manufacturer_selection != "" and label_selection != "" and date_selection != None and comment_selection != "" and status_selection != None and condition_selection != None):
            st.error("One or more required fields are not filled in.")
        else:
            try:
                cur.execute("SELECT MAX(equip_id) FROM Equipment;")
                maxID = cur.fetchall()[0][0]
                
                cur.execute("""
                INSERT INTO Equipment (equip_id, serial_number, product_name, manufacturer, label, category, purchase_date, comments, \"status\", condition)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, (maxID+1, serial_selection, product_selection, manufacturer_selection, label_selection, "Miscellaneous", date_selection, comment_selection, status_selection, condition_selection))

                conn.commit()
                st.success("Item sucessfully added.")
                st.session_state['add_edit_remove'] = 0
                time.sleep(1)
                st.rerun()
            except Exception as err:
                print_psycopg2_exception(err)
                conn.rollback()

def display_add_items():
    selection = st.selectbox('What type of item would you like to add?',
    ('Mobile Device', 'Camera', 'Computer', 'FPGA Board', 'VR/AR', 'Miscellaneous'))

    if selection == "Mobile Device":
        display_mobile_device_entry()
    elif selection == "Camera":
        display_camera_entry()
    elif selection == "Computer":
        display_computer_entry()
    elif selection == "FPGA Board":
        display_fpga_entry()
    elif selection == "VR/AR":
        display_vrar_entry()
    elif selection == "Miscellaneous":
        display_other_entry()

def info_callback(value):

    cur.execute(f"""
    SELECT COUNT(*)
    FROM Equipment
    WHERE equip_id = {value};
    """)
    if cur.fetchall()[0][0] == 1:
        try:
            # Get the category of the item
            cur.execute(f"""
            SELECT Category
            FROM Equipment
            WHERE equip_id = {value};
            """)
            category = cur.fetchall()[0][0]

            # Create a query based on the category
            if category == "Mobile Devices":
                cur.execute(f"SELECT * FROM MobileDevice WHERE equip_id={value}")
                raw_data = cur.fetchall()
                column_names = ['ID#', 'Mobile Type', 'Chipset', 'Operating System', 'RAM', 'Storage', 'IP Address']
                data_frame = pd.DataFrame(raw_data, columns=column_names)
                st.dataframe(data_frame)

            elif category == "Camera":
                cur.execute(f"SELECT * FROM Camera WHERE equip_id={value}")
                raw_data = cur.fetchall()
                column_names = ['ID#', 'Camera Type', 'Resolution', 'Megapixels', 'SD Card']
                data_frame = pd.DataFrame(raw_data, columns=column_names)
                st.dataframe(data_frame)

            elif category == "Computer":
                cur.execute(f"SELECT * FROM Computer WHERE equip_id={value}")
                raw_data = cur.fetchall() 
                column_names = ['ID#', 'Computer Type', 'CPU', 'GPU', 'RAM', 'Storage', 'Host Name', 'Operating System', 'Local Admin', 'IP Address']
                data_frame = pd.DataFrame(raw_data, columns=column_names)
                st.dataframe(data_frame)

            elif category == "FPGA Board":
                cur.execute(f"SELECT * FROM FPGADeviceBoard WHERE equip_id={value}")
                raw_data = cur.fetchall()
                column_names = ['ID#', 'Board Type', 'Storage']
                data_frame = pd.DataFrame(raw_data, columns=column_names)
                st.dataframe(data_frame)

            elif category == "VR/AR Device":
                cur.execute(f"SELECT * FROM VRARDevice WHERE equip_id={value}")
                raw_data = cur.fetchall()
                column_names = ['ID#', 'Storage']
                data_frame = pd.DataFrame(raw_data, columns=column_names)
                st.dataframe(data_frame)

            elif category == "Miscellaneous":
                st.error('Miscellaneous Item: No futher information available.')

        except Exception as err:
            print_psycopg2_exception(err)
            conn.rollback()
    else:
        st.error("Equip_id invalid. ID must be present and unique.")

def display_info_items():
    eid = st.number_input('Select the ID# of the item you\'d like to examine:', min_value=1, value=None, step=1)
    if st.button('Confirm') and eid != None:
        info_callback(eid)

def execute_edit_sql(category, attribute, new_input, equip_id):
    if attribute == "Serial Number":
        cur.execute(f"""
        UPDATE Equipment SET serial_number = \'{new_input}\'
        WHERE equip_id = {equip_id};
        """)
    elif attribute == "Product Name":
        cur.execute(f"""
        UPDATE Equipment SET product_name = \'{new_input}\'
        WHERE equip_id = {equip_id};
        """)
    elif attribute == "Manufacturer":
        cur.execute(f"""
        UPDATE Equipment SET manufacturer = \'{new_input}\'
        WHERE equip_id = {equip_id};
        """)
    elif attribute == "Label":
        cur.execute(f"""
        UPDATE Equipment SET label = \'{new_input}\'
        WHERE equip_id = {equip_id};
        """)
    elif attribute == "Comments":
        cur.execute(f"""
        UPDATE Equipment SET  = \'{new_input}\'
        WHERE equip_id = {equip_id};
        """)
    elif attribute == "Chipset" and category == "Mobile Devices":
        cur.execute(f"""
        UPDATE MobileDevice SET chipset = \'{new_input}\'
        WHERE equip_id = {equip_id};
        """)
    elif attribute == "Operating System" and category == "Mobile Devices":
        cur.execute(f"""
        UPDATE Equipment SET operating_system = \'{new_input}\'
        WHERE equip_id = {equip_id};
        """)
    elif attribute == "RAM" and category == "Mobile Devices":
        cur.execute(f"""
        UPDATE Equipment SET ram = \'{new_input}\'
        WHERE equip_id = {equip_id};
        """)
    elif attribute == "Storage" and category == "Mobile Devices":
        cur.execute(f"""
        UPDATE Equipment SET  = \'{new_input}\'
        WHERE equip_id = {equip_id};
        """)
    elif attribute == "Resolution" and category == "Camera":
        cur.execute(f"""
        UPDATE Camera SET resolution = \'{new_input}\'
        WHERE equip_id = {equip_id};
        """)
    elif attribute == "Megapixels" and category == "Camera":
        cur.execute(f"""
        UPDATE Camera SET megapixels = \'{new_input}\'
        WHERE equip_id = {equip_id};
        """)
    elif attribute == "SD Card" and category == "Camera":
        cur.execute(f"""
        UPDATE Camera SET sd_card = \'{new_input}\'
        WHERE equip_id = {equip_id};
        """)
    elif attribute == "CPU" and category == "Computer":
        cur.execute(f"""
        UPDATE Computer SET cpu = \'{new_input}\'
        WHERE equip_id = {equip_id};
        """)
    elif attribute == "GPU" and category == "Computer":
        cur.execute(f"""
        UPDATE Computer SET gpu = \'{new_input}\'
        WHERE equip_id = {equip_id};
        """)
    elif attribute == "RAM" and category == "Computer":
        cur.execute(f"""
        UPDATE Computer SET ram = \'{new_input}\'
        WHERE equip_id = {equip_id};
        """)
    elif attribute == "Storage" and category == "Computer":
        cur.execute(f"""
        UPDATE Computer SET storage = \'{new_input}\'
        WHERE equip_id = {equip_id};
        """)
    elif attribute == "Host Name" and category == "Computer":
        cur.execute(f"""
        UPDATE Computer SET host_name = \'{new_input}\'
        WHERE equip_id = {equip_id};
        """)
    elif attribute == "Operating System" and category == "Computer":
        cur.execute(f"""
        UPDATE Computer SET operating_system = \'{new_input}\'
        WHERE equip_id = {equip_id};
        """)
    elif attribute == "Local Admin" and category == "Computer":
        cur.execute(f"""
        UPDATE Computer SET local_admin = \'{new_input}\'
        WHERE equip_id = {equip_id};
        """)
    elif attribute == "Storage" and category == "FPGA Board":
        cur.execute(f"""
        UPDATE FPGADeviceBoard SET storage = \'{new_input}\'
        WHERE equip_id = {equip_id};
        """)
    elif attribute == "Storage" and category == "VR/AR Device":
        cur.execute(f"""
        UPDATE VRARDevice SET storage = \'{new_input}\'
        WHERE equip_id = {equip_id};
        """)
    else:
        st.error("Related query for entry could not be found, this shouldn't happen during operation.")

def edit_input_fields(category, attribute, equip_id):

    # Do the special case scenarios where there is a different kind of entry that isn't text        
    if attribute == "Purchase Date":
        new_input = st.date_input('Provide modified entry below:', format="MM/DD/YYYY", value=None)
        if st.button('Submit'):
            if new_input != None:
                # try to modify the entry
                try:
                    cur.execute(f"""
                    UPDATE Equipment SET purchase_date = \'{new_input}\'
                    WHERE equip_id = {equip_id};
                    """)
                    conn.commit()
                    st.success("Item sucessfully modified.")
                    time.sleep(1)
                    st.session_state['add_edit_remove'] = 0
                    st.session_state['edit_display'] = 0
                    st.rerun()
                except Exception as err:
                    st.error(print_psycopg2_exception(err))
                    conn.rollback()
            elif new_input == None:
                st.error("Entry cannot be empty.")
    elif attribute == "Condition":
        new_input = st.selectbox('Provide modified entry below:', ('Good', 'Issues', 'Broken'), index=None)
        if st.button('Submit'):
            if new_input != None:
                # try to modify the entry
                try:
                    cur.execute(f"""
                    UPDATE Equipment SET condition = \'{new_input}\'
                    WHERE equip_id = {equip_id};
                    """)
                    conn.commit()
                    st.success("Item sucessfully modified.")
                    time.sleep(1)
                    st.session_state['add_edit_remove'] = 0
                    st.session_state['edit_display'] = 0
                    st.rerun()
                except Exception as err:
                    st.error(print_psycopg2_exception(err))
                    conn.rollback()
            elif new_input == None:
                st.error("Entry cannot be empty.")
    elif attribute == "Mobile Type":
        new_input = st.selectbox('Provide modified entry below:', ('Smartphone', 'Other'), index=None)
        if st.button('Submit'):
            if new_input != None:
                # try to modify the entry
                try:
                    cur.execute(f"""
                    UPDATE MobileDevice SET mobile_type = \'{new_input}\'
                    WHERE equip_id = {equip_id};
                    """)
                    conn.commit()
                    st.success("Item sucessfully modified.")
                    time.sleep(1)
                    st.session_state['add_edit_remove'] = 0
                    st.session_state['edit_display'] = 0
                    st.rerun()
                except Exception as err:
                    st.error(print_psycopg2_exception(err))
                    conn.rollback()
            elif new_input == None:
                st.error("Entry cannot be empty.")
    elif attribute == "IP Address" and category == "Mobile Devices":
        new_input = st.text_input('Provide modified entry below:', max_chars=45)
        if st.button('Submit'):
            if new_input != None:
                # try to modify the entry
                try:
                    cur.execute(f"""
                    UPDATE MobileDevice SET ip_address = \'{new_input}\'
                    WHERE equip_id = {equip_id};
                    """)
                    conn.commit()
                    st.success("Item sucessfully modified.")
                    time.sleep(1)
                    st.session_state['add_edit_remove'] = 0
                    st.session_state['edit_display'] = 0
                    st.rerun()
                except Exception as err:
                    st.error(print_psycopg2_exception(err))
                    conn.rollback()
            elif new_input == "":
                st.error("Entry cannot be empty.")
    elif attribute == "IP Address" and category == "Computer":
        new_input = st.text_input('Provide modified entry below:', max_chars=45)
        if st.button('Submit'):
            if new_input != None:
                # try to modify the entry
                try:
                    cur.execute(f"""
                    UPDATE Computer SET ip_address = \'{new_input}\'
                    WHERE equip_id = {equip_id};
                    """)
                    conn.commit()
                    st.success("Item sucessfully modified.")
                    time.sleep(1)
                    st.session_state['add_edit_remove'] = 0
                    st.session_state['edit_display'] = 0
                    st.rerun()
                except Exception as err:
                    st.error(print_psycopg2_exception(err))
                    conn.rollback()
            elif new_input == "":
                st.error("Entry cannot be empty.")
    elif attribute == "Camera Type":
        new_input = st.selectbox('Provide modified entry below:', ('DSLR', 'Mirrorless', 'Point and Shoot', 'Action', '360', 'Drone', 'Other'), index=None)
        if st.button('Submit'):
            if new_input != None:
                # try to modify the entry
                try:
                    cur.execute(f"""
                    UPDATE Camera SET camera_type = \'{new_input}\'
                    WHERE equip_id = {equip_id};
                    """)
                    conn.commit()
                    st.success("Item sucessfully modified.")
                    time.sleep(1)
                    st.session_state['add_edit_remove'] = 0
                    st.session_state['edit_display'] = 0
                    st.rerun()
                except Exception as err:
                    st.error(print_psycopg2_exception(err))
                    conn.rollback()
            elif new_input == None:
                st.error("Entry cannot be empty.")
    elif attribute == "Computer Type":
        new_input = st.selectbox('Provide modified entry below:', ('Desktop', 'Laptop', 'Server', 'Mainframe', 'Other'), index=None)
        if st.button('Submit'):
            if new_input != None:
                # try to modify the entry
                try:
                    cur.execute(f"""
                    UPDATE Computer SET computer_type = \'{new_input}\'
                    WHERE equip_id = {equip_id};
                    """)
                    conn.commit()
                    st.success("Item sucessfully modified.")
                    time.sleep(1)
                    st.session_state['add_edit_remove'] = 0
                    st.session_state['edit_display'] = 0
                    st.rerun()
                except Exception as err:
                    st.error(print_psycopg2_exception(err))
                    conn.rollback()
            elif new_input == None:
                st.error("Entry cannot be empty.")
    elif attribute == "Board Type":
        new_input = st.selectbox('Provide modified entry below:', ('FPGA', 'Microcontroller', 'Other'), index=None)
        if st.button('Submit'):
            if new_input != None:
                # try to modify the entry
                try:
                    cur.execute(f"""
                    UPDATE FPGADeviceBoard SET board_type = \'{new_input}\'
                    WHERE equip_id = {equip_id};
                    """)
                    conn.commit()
                    st.success("Item sucessfully modified.")
                    time.sleep(1)
                    st.session_state['add_edit_remove'] = 0
                    st.session_state['edit_display'] = 0
                    st.rerun()
                except Exception as err:
                    st.error(print_psycopg2_exception(err))
                    conn.rollback()
            elif new_input == None:
                st.error("Entry cannot be empty.")
    else: # It's just a normal text entry
        new_input = st.text_input('Provide modified entry below:', max_chars=255)
        if st.button('Submit'):
            if new_input != "":
                # try to modify the entry
                try:
                    execute_edit_sql(category, attribute, new_input, equip_id)
                    conn.commit()
                    st.success("Item sucessfully modified.")
                    time.sleep(1)
                    st.session_state['add_edit_remove'] = 0
                    st.session_state['edit_display'] = 0
                    st.rerun()
                except Exception as err:
                    st.error(print_psycopg2_exception(err))
                    conn.rollback()
            elif new_input == "":
                st.error("Entry cannot be empty.")

def edit_callback(value):
    cur.execute(f"""
    SELECT COUNT(*)
    FROM Equipment
    WHERE equip_id = {value};
    """)
    if cur.fetchall()[0][0] == 1:
        try:
            # Get the category of the item
            cur.execute(f"""
            SELECT Category
            FROM Equipment
            WHERE equip_id = {value};
            """)
            category = cur.fetchall()[0][0]

            # Populate a dropdown based on the category received
            # equip_id,serial_number,product_name,manufacturer,label,category,purchase_date,comments,status,condition

            if category == "Mobile Devices": #equip_id,mobile_type,chipset,operating_system,ram,storage,ip_address
                attributes = ('Serial Number', 'Product Name', 'Manufacturer', 'Label', 'Purchase Date', 'Comments', 'Condition',  'Mobile Type', 'Chipset', 'Operating System', 'RAM', 'Storage', 'IP Address')
            elif category == "Camera": # equip_id,camera_type,resolution,megapixels,sd_card
                attributes = ('Serial Number', 'Product Name', 'Manufacturer', 'Label', 'Purchase Date', 'Comments', 'Condition', 'Camera Type', 'Resolution', 'Megapixels', 'SD Card')
            elif category == "Computer": # equip_id,computer_type,cpu,gpu,ram,storage,hostname,operating_system,local_admin,ip_address
                attributes = ('Serial Number', 'Product Name', 'Manufacturer', 'Label', 'Purchase Date', 'Comments', 'Condition', 'Computer Type', 'CPU', 'GPU', 'RAM', 'Storage', 'Host Name', 'Operating System', 'Local Admin', 'IP Address')
            elif category == "FPGA Board": # equip_id,board_type,storage
                attributes = ('Serial Number', 'Product Name', 'Manufacturer', 'Label', 'Purchase Date', 'Comments', 'Condition', 'Board Type', 'Storage')
            elif category == "VR/AR Device":
                attributes = ('Serial Number', 'Product Name', 'Manufacturer', 'Label', 'Purchase Date', 'Comments', 'Condition', 'Storage')
            elif category == "Miscellaneous":
                attributes = ('Serial Number', 'Product Name', 'Manufacturer', 'Label', 'Purchase Date', 'Comments', 'Condition')

            selected_attr = st.selectbox('Which attribute would you like to edit?', attributes)
            edit_input_fields(category, selected_attr, value)

        except Exception as err:
            print_psycopg2_exception(err)
            conn.rollback()
    else:
        st.error("Equip_id invalid. ID must be present and unique.")

def display_edit_items():
    eid = st.number_input('Select the ID# of the item you\'d like to edit:', min_value=1, value=None, step=1)
    if (st.button('Confirm') and eid != None) or st.session_state['edit_display']:
        st.session_state['edit_display'] = 1
        edit_callback(eid)

def display_add_edit_remove_items(value):
    if value == 1:
        st.write("#### Add Item")
        display_add_items()
    elif value == 2:
        st.write("#### Edit Item")
        display_edit_items()
    elif value == 3:
        st.write("#### Remove Item")
        display_remove_items()
    elif value == 4:
        st.write("#### More Item Info")
        display_info_items()

def display_home_table(value):
    if value == 1:
        st.write("Displaying All Items:")
        display_all_table()

        if st.session_state['user_role'] == "admin":
            col1, col2, col3, col4 = st.columns([0.9,1.15,0.9,3.4])
            if col1.button('Add Item'):
                st.session_state['add_edit_remove'] = 1
            if col2.button('Remove Item'):
                st.session_state['add_edit_remove'] = 3
            if col3.button('Edit Item'):
                st.session_state['add_edit_remove'] = 2
                st.session_state['edit_display'] = 0
            if col4.button('More Item Info'):
                st.session_state['add_edit_remove'] = 4

            display_add_edit_remove_items(st.session_state['add_edit_remove'])
        
    elif value == 2:
        st.write("Displaying Checked Out Items:")
        display_out_table()
    elif value == 3:
        st.write("Displaying Available Items:")
        display_in_table()
    elif value == 4:
        st.write("Displaying Transaction History:")
        display_hist_table()

def logout():
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()

user_name = st.session_state.get('user_name')

##################################################################
###--------------------- APPLICATION MAIN ---------------------###
##################################################################

if not st.session_state['logged_in']:
    username, password, user_type = show_login_form()
    user_role = check_credentials(username, password, user_type)
    if user_role:
        st.session_state['logged_in'] = True
        st.session_state['user_role'] = user_role
        st.session_state['user_id'] = username #Store the user ID in the session state = global variable
        
        st.rerun()
else:
    st.title("Inventory")
    st.write(f"Hi {user_name}, browse our inventory for devices.")

    col1, col2, col3, col4 = st.columns([0.9,1.15,0.95,3])

    if st.sidebar.button("Logout"):
        logout()

    if col1.button('All Items'):
        st.session_state['homeview'] = 1
        st.session_state['add_edit_remove'] = 0

    if col2.button('Checked Out'):
        st.session_state['homeview'] = 2
        st.session_state['add_edit_remove'] = 0

    if col3.button('Available'):
        st.session_state['homeview'] = 3
        st.session_state['add_edit_remove'] = 0

    if col4.button('Transaction History'):
        if st.session_state['user_role'] == "admin":
            st.session_state['homeview'] = 4
            st.session_state['add_edit_remove'] = 0
        else:
            st.error("You do not have the privileges to view this content.")

    display_home_table(st.session_state['homeview'])