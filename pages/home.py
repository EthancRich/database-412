# home.py
import streamlit as st
import psycopg2

#if not logged in dont show anything
if not st.session_state.get('logged_in', False):
    st.error("You are not logged in.")
    st.stop()

def logout():
        for key in st.session_state.keys():
            del st.session_state[key]
        st.experimental_rerun()

if st.sidebar.button("Logout"):
    logout()

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

def display_available_items():
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM equipment WHERE status = 'Available';")
    rows = cur.fetchall()
    for row in rows:
        st.write(row)
    conn.close()

# Writing things here
st.title("Home Page")
st.write("Welcome to the Lab Equipment Inventory System!")
display_available_items()