import streamlit as st
import pandas as pd
import psycopg2
from psycopg2 import sql

# Define function to connect to your PostgreSQL database
def connect_to_db():
    conn = psycopg2.connect(
        host="127.0.0.1",
        port="8888",
        database="db",
        user="nbalamur",
        password=""
    )
    return conn

# Define function to get available items from the database
def get_available_items(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM Users;")
        rows = cur.fetchmany(size=10)
        return pd.DataFrame(rows, columns=['ID', 'Name'])

# Login Section

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False


# Define the login form in the sidebar only if the user is not authenticated
if not st.session_state['authenticated']:
    with st.sidebar:
        user_id = st.text_input('User ID')
        password = st.text_input('Password', type='password')
        if st.button('Login'):
            # Add authentication logic here
            if user_id == "asu" and password == "123":  # Example condition
                st.session_state['authenticated'] = True
                st.success("You are now logged in!")
            else:
                st.error("Incorrect User ID or Password")


# If the user is authenticated, do not show the sidebar content
# Continue with the rest of your Streamlit app main body
if st.session_state['authenticated']:
    st.success("Logged in as {}".format(user_id))
    st.write("Welcome to the VR research lab inventory system!")
    # Once logged in, show the available items in a table
    # Once logged in, show the available items in a table
    conn = connect_to_db()
    try:
        df_items = get_available_items(conn)
        st.write("Available Items:")
        st.dataframe(df_items)
    except Exception as e:
        st.error("Error: %s" % str(e))
    finally:
        conn.close()
else:
    st.write("Please log in to view the inventory system.")

# The rest of your Streamlit code for item checkout, return, delete, etc., would go here