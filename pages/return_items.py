# return_items.py
import datetime
import streamlit as st
import psycopg2
import pandas as pd

#if not logged in dont show anything
if not st.session_state.get('logged_in', False):
    st.error("You are not logged in.")
    st.stop()

if 'has_items' not in st.session_state:
    st.session_state['has_items'] = 1

def logout():
        for key in st.session_state.keys():
            del st.session_state[key]
        st.experimental_rerun()
if st.sidebar.button("Logout"):
    logout()

user_id = st.session_state.get('user_id') #accessing gloabal userID variable from login
user_name = st.session_state.get('user_name')

st.title("Return Items")
st.write("This page allows you to return borrowed items.")


#TO DO: Add functionalities to list borrowed items and manage returns
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

def display_user_equipment_table():
    #function to display the equipment table
    with connect_to_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT DISTINCT(Equipment.equip_id), Equipment.product_name, Equipment.manufacturer, Equipment.condition, Equipment.comments, Transaction.checkout_date, Transaction.expected_return_date FROM Transaction, Equipment WHERE Equipment.equip_id=Transaction.equipment_items[1] AND Transaction.users_id=%s AND Transaction.actual_return_date=%s;", (user_id, datetime.date(datetime.MINYEAR, 1, 1),))
            raw_data = cur.fetchall()
            if raw_data == []:
                st.session_state['has_items'] = 0
            else:
                st.session_state['has_items'] = 1
            column_names = ["Equipment ID", "Equipment Name", "Manufacturer", "Condition", "Comments", "Checkout Date", "Expected Return Date"]
    data_frame = pd.DataFrame(raw_data, columns=column_names)
    st.dataframe(data_frame)  # Or st.table(data_frame)

def get_available_equipment_ids():
    #function to get "Available" equipment ids from the database
    with connect_to_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT equip_id FROM Equipment, Transaction WHERE Equipment.equip_id=Transaction.equipment_items[1] AND Transaction.users_id=%s AND Transaction.actual_return_date=%s;", (user_id, datetime.date(datetime.MINYEAR, 1, 1),))
            equipment_ids = [row[0] for row in cur.fetchall()]
    return equipment_ids

def display_return_form():
    #Displays the Return form
    st.subheader("Return Equipment")
    st.write(f"Returning as {user_name} ({user_id})")
    available_ids = get_available_equipment_ids()
    selected_id = st.selectbox("Select Equipment ID to return:", available_ids)
    # condition = st.
    with connect_to_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT Equipment.condition FROM Equipment WHERE Equipment.equip_id=%s;",(selected_id,))
            current_condition = cur.fetchall()

            cur.execute("SELECT DISTINCT(Equipment.comments) FROM Equipment WHERE Equipment.equip_id=%s;",(selected_id,))
            current_comments = cur.fetchall()

    condition = st.selectbox("Condition:", ['Good', 'Issues', 'Broken'])
    comments = st.text_area("Comments:", current_comments[0][0])
    
    if st.button("Return"):
        if selected_id and user_id:
            process_return(user_id, [selected_id], condition, comments)
        else:
            st.error("Please enter the required information.")



def process_return(user_id, selected_equipment_ids, condition, comments):
    #Changes the status of the equipment to "Available" and updates row in the Transaction table
    actual_return_date = datetime.date.today() # Current date
    with connect_to_db() as conn:
        with conn.cursor() as cur:
            # Update Equipment table
            for equip_id in selected_equipment_ids:
                cur.execute("UPDATE Equipment SET status = 'Available', condition=%s, comments=%s WHERE equip_id=%s;", (condition, comments,equip_id,))
                cur.execute("UPDATE Transaction SET actual_return_date=%s WHERE equipment_items=%s;", (actual_return_date, [equip_id],))

            # Update Transaction table
            conn.commit()

    st.success(f"Equipment returned successfully.")
    st.rerun() # Refresh the page to reflect the updated status

st.write("Here are your checked out items:")
display_user_equipment_table() #Display data
if st.session_state['has_items']:
    display_return_form() #Display return form
else:
    st.write('You currently have no items checked out!')