# checkout.py
import datetime
import streamlit as st
import psycopg2
import pandas as pd

#if not logged in dont show anything
#if not st.session_state.get('logged_in', False):
 #   st.error("You are not logged in.")
 #   st.stop()

#display logout button
def logout():
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()
if st.sidebar.button("Logout"):
        logout()

#titles
user_name = st.session_state.get('user_name')
st.title(f"Hi {user_name}, Check Out Items")   


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

def display_equipment_table():
    #function to display the equipment table
    with connect_to_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT equip_id, product_name, manufacturer, condition, comments FROM Equipment WHERE status = 'Available';")
            raw_data = cur.fetchall()
            column_names = ["Equipment ID", "Equipment Name", "Manufacturer", "Condition", "Comments"]
    data_frame = pd.DataFrame(raw_data, columns=column_names)
    st.dataframe(data_frame)  # Or st.table(data_frame)

st.write("Here are the available items:")
display_equipment_table() #Display data


def display_transaction_table():
    with connect_to_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM Transaction;")
            raw_data = cur.fetchall()
    data_frame = pd.DataFrame(raw_data)
    st.dataframe(data_frame)  # Or st.table(data_frame)


def get_available_equipment_ids():
    #function to get "Available" equipment ids from the database
    with connect_to_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT equip_id FROM Equipment WHERE status = 'Available'")
            equipment_ids = [row[0] for row in cur.fetchall()]
    return equipment_ids


def display_checkout_form():
    #Displays the checkout form
    st.subheader("Checkout Equipment")
    user_id = st.session_state.get('user_id') #accessing gloabal userID variable from login
    st.write(f"Checking out as {user_name} ({user_id})")
    available_ids = get_available_equipment_ids()
    selected_id = st.selectbox("Select Equipment ID to checkout:", available_ids)
    expected_return_date = st.date_input("Expected Return Date:")
    comments = st.text_area("Comments:")
    
    if st.button("Checkout"):
        if selected_id and user_id:
            process_checkout(user_id, [selected_id], expected_return_date, comments)
        else:
            st.error("Please enter the required information.")



def process_checkout(user_id, selected_equipment_ids, expected_return_date, comments=""):
    #Changes the status of the equipment to "Unavailable" and adds a new row to the Transaction table
    trans_id = get_next_transaction_id() 

    with connect_to_db() as conn:
        with conn.cursor() as cur:
            # Update Equipment table
            for equip_id in selected_equipment_ids:
                cur.execute("UPDATE Equipment SET status = 'Unavailable' WHERE equip_id = %s", (equip_id,))

            # Insert into Transaction table
            checkout_date = datetime.date.today() # Current date
            cur.execute("INSERT INTO Transaction (trans_id, users_id, equipment_items, checkout_date, expected_return_date, comments) VALUES (%s, %s, %s, %s, %s, %s)", 
                        (trans_id, user_id, selected_equipment_ids, checkout_date, expected_return_date, comments))

            conn.commit()

    st.success(f"Equipment checked out successfully. Transaction ID: {trans_id}")
    st.rerun() # Refresh the page to reflect the updated status


def get_next_transaction_id():
    #function to get the next transaction ID from the database
    with connect_to_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT MAX(trans_id) FROM Transaction")
            max_id = cur.fetchone()[0]
            return max_id + 1 if max_id is not None else 1


#Display checkout form
display_checkout_form()
display_transaction_table() #TODO: Remove this later