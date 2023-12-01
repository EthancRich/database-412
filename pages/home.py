# home.py
import streamlit as st
import psycopg2
import pandas as pd

#if not logged in dont show anything
# if not st.session_state.get('logged_in', False):
#     st.error("You are not logged in.")
#     st.stop()

# homeview describes the main table being displayed each run.
#   0 - no table to display.
#   1 - all table
#   2 - out table
#   3 - in table
#   4 - hist table
if 'homeview' not in st.session_state:
    st.session_state['homeview'] = 0

def logout():
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

def connect_to_db():
    #Connect to database and close connection on demand
    conn = psycopg2.connect(
        host="bubble.db.elephantsql.com",
        port="5432",
        database="ozhptawz",
        user="ozhptawz",
        password="rw1e9fAoDhnYmq4D2QKgu51o4g7zS-fJ" #THIS IS UNSAFE. REMOVE THIS IN THE FUTURE.
    )
    return conn

conn = connect_to_db()
cur = conn.cursor()

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

def display_hist_table(): # trans_id,users_id,equipment_items,checkout_date,expected_return_date,actual_return_date,comments
    cur.execute("""
        SELECT users_id, equipment_items, checkout_date, expected_return_date, actual_return_date, comments 
        FROM Transaction;
        """)
    raw_data = cur.fetchall()
    column_names = ['ASURITE', 'Equipment IDs', 'Checked Out', 'Return Due', 'Checked In', 'Comments']
    data_frame = pd.DataFrame(raw_data, columns=column_names)
    st.dataframe(data_frame)

def display_home_table(value):
    if value == 1:
        display_all_table()
    elif value == 2:
        display_out_table()
    elif value == 3:
        display_in_table()
    elif value == 4:
        display_hist_table()

###--------------------- DRAWING THE PAGE ---------------------###

st.title("Home Page")
st.write("Welcome to the Lab Equipment Inventory System!")

col1, col2, col3, col4 = st.columns([0.9,1.15,0.95,3])

if st.sidebar.button("Logout"):
    logout()

if col1.button('All Items'):
    st.session_state['homeview'] = 1

if col2.button('Checked Out'):
    st.session_state['homeview'] = 2

if col3.button('Available'):
    st.session_state['homeview'] = 3

if col4.button('Transaction History'):
    if st.session_state['user_role'] == "admin":
        st.session_state['homeview'] = 4
    else:
        st.error("You do not have the privileges to view this content.")

display_home_table(st.session_state['homeview'])

# option = st.selectbox(
#     'How would you like to be contacted?',
#     ('Email', 'Home phone', 'Mobile phone'))