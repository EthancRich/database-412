# home.py
import streamlit as st
import psycopg2
import pandas as pd
import sys
import time

###---------- INTIALIZATION ----------###

# Prevent usage if not logged in
# if not st.session_state.get('logged_in', False):
#     st.error("You are not logged in.")
#     st.stop()

# homeview describes the main table being displayed each run.
#   0 - no table to display.    1 - all table
#   2 - out table               3 - in table            4 - hist table
if 'homeview' not in st.session_state:
    st.session_state['homeview'] = 0

# add_edit_remove tells which button menu is currently being used.
#   0 - no button being used.   1 - Add button
#   2 - Edit button             3 - Remove button
if 'add_edit_remove' not in st.session_state:
    st.session_state['add_edit_remove'] = 0

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
    print ("\nextensions.Diagnostics:", err.diag)

    # print the pgcode and pgerror exceptions
    print ("pgerror:", err.pgerror)
    print ("pgcode:", err.pgcode, "\n")

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
                cur.execute("""
                INSERT INTO Equipment (serial_number, product_name, manufacturer, label, category, purchase_date, comments, \"status\", condition)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, (serial_selection, product_selection, manufacturer_selection, label_selection, "Mobile Devices", date_selection, comment_selection, status_selection, condition_selection))
                cur.execute(f"""
                INSERT INTO MobileDevice ()
                VALUES ();
                """)

                conn.commit()
                st.success("Item sucessfully added.")
                time.sleep(1)
                st.rerun()
            except Exception as err:
                print_psycopg2_exception(err)
                conn.rollback()
            

def display_add_items():
    selection = st.selectbox('What type of item would you like to add?',
    ('Mobile Device', 'Camera', 'Computer', 'FPGA Board', 'VR/AR', 'Other'))

    if selection == "Mobile Device":
        display_mobile_device_entry()
    elif selection == "Camera":
        pass
    elif selection == "Computer":
        pass
    elif selection == "FPGA Board":
        pass
    elif selection == "VR/AR":
        pass
    elif selection == "Other":
        pass

def display_add_edit_remove_items(value):
    if value == 1:
        display_add_items()
    elif value == 2:
        pass
    elif value == 3:
        display_remove_items()

def display_home_table(value):
    if value == 1:
        display_all_table()

        if st.session_state['user_role'] == "admin":
            col1, col2, col3 = st.columns([0.9,1.15,4])
            if col1.button('Add Item'):
                st.session_state['add_edit_remove'] = 1
            if col2.button('Remove Item'):
                st.session_state['add_edit_remove'] = 3
            if col3.button('Edit Item'):
                st.session_state['add_edit_remove'] = 2

            display_add_edit_remove_items(st.session_state['add_edit_remove'])
        
    elif value == 2:
        display_out_table()
    elif value == 3:
        display_in_table()
    elif value == 4:
        display_hist_table()

def logout():
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()

###--------------------- DRAWING THE PAGE ---------------------###

st.title("Home Page")
st.write("Welcome to the Lab Equipment Inventory System!")

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