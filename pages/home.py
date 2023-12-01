# home.py
import streamlit as st
import psycopg2
import pandas as pd

#if not logged in dont show anything
# if not st.session_state.get('logged_in', False):
#     st.error("You are not logged in.")
#     st.stop()

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


###--------------------- DRAWING THE PAGE ---------------------###

st.title("Home Page")
st.write("Welcome to the Lab Equipment Inventory System!")

col1, col2, col3, col4 = st.columns([0.9,1.15,0.95,3])

if st.sidebar.button("Logout"):
    logout()

if col1.button('All Items'):
    display_all_table()

if col2.button('Checked Out'):
    display_out_table()

if col3.button('Available'):
    display_in_table()

if col4.button('Transaction History'):
    if st.session_state['user_role'] == "admin":
        display_hist_table()
    else:
        st.error("You do not have the privileges to view this content.")
