# checkout.py
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
        st.experimental_rerun()
if st.sidebar.button("Logout"):
        logout()

#titles
st.title("Check Out Items")   
st.write("Here are the available items:")

# TO DO: Add forms, tables, or other elements to manage item checkout

#Connect to database
# Define function to connect to your PostgreSQL database
#Connect to database and close connection on demand
def connect_to_db():
    conn = psycopg2.connect(
        host="bubble.db.elephantsql.com",
        port="5432",
        database="ozhptawz",
        user="ozhptawz",
        password="rw1e9fAoDhnYmq4D2QKgu51o4g7zS-fJ" #THIS IS UNSAFE. REMOVE THIS IN THE FUTURE.
    )
    return conn

def display_data():
    with connect_to_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT equip_id, product_name, manufacturer, condition, comments FROM Equipment WHERE status = 'Available';")
            raw_data = cur.fetchall()
            column_names = ["Equipment ID", "Equipment Name", "Manufacturer", "Condition", "Comments"]
    data_frame = pd.DataFrame(raw_data, columns=column_names)
    st.dataframe(data_frame)  # Or st.table(data_frame)

display_data() #Display data

#Allow user to select items and checkout
#Define function to get available equipment ids from the database
def get_available_equipment_ids():
    with connect_to_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT equip_id FROM Equipment WHERE status = 'Available'")
            equipment_ids = [row[0] for row in cur.fetchall()]
    return equipment_ids

def display_checkout_form():
    st.subheader("Checkout Equipment")
    available_ids = get_available_equipment_ids()

    # Check if there are available IDs
    if available_ids:
        selected_id = st.selectbox("Select Equipment ID to checkout:", available_ids)
        if st.button("Checkout"):
            process_checkout(selected_id)
    else:
        st.write("No available equipment for checkout.")


def process_checkout(equip_id):
    # Implement the logic to checkout the equipment
    # This involves updating the status of the equipment in the database
    # Example:
    with connect_to_db() as conn:
        with conn.cursor() as cur:
            # Example SQL query, adjust according to your database schema
            cur.execute("UPDATE Equipment SET status = 'Unavailable' WHERE equip_id = %s", (equip_id,))
            conn.commit()
    st.success(f"Equipment ID {equip_id} checked out successfully.")
    st.experimental_rerun() # Refresh the page to reflect the updated status

#Display checkout form
display_checkout_form()