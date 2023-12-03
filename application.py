import streamlit as st
import pandas as pd
import psycopg2
from psycopg2 import sql

#Import the different pages 
# from pages.home import show as show_home
# from pages.checkout import show as show_checkout
# from pages.return_items import show as show_return_items

# Define function to get available items from the database
def get_available_items(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM Users;")
        rows = cur.fetchmany(size=10)
        return pd.DataFrame(rows, columns=['ID', 'Name'])

def load_users_from_csv(file_path):
    #Load the CSV file into a pandas dataframe
    df = pd.read_csv(file_path)
    users = {row['users_id']: {"password": "123", "role": "student", "name": row['users_name']} for index, row in df.iterrows()}
    
    # Add a manual entry for the admin user
    users['admin'] = {"password": "adminpass", "role": "admin", "name": "Admin User"}

    return users


users = load_users_from_csv("CSVFiles/Users.csv")


# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

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

#username, password, user_type = show_login_form()
#user_role = check_credentials(username, password, user_type)

# Initialize session state for login status
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['user_role'] = None

if not st.session_state['logged_in']:
    username, password, user_type = show_login_form()
    user_role = check_credentials(username, password, user_type)
    if user_role:
        st.session_state['logged_in'] = True
        st.session_state['user_role'] = user_role
        st.session_state['user_id'] = username #Store the user ID in the session state = global variable
        
        st.experimental_rerun()
else:
    
    # Function to handle logout
    def logout():
        for key in st.session_state.keys():
            del st.session_state[key]
        st.experimental_rerun()
    if st.sidebar.button("Logout"):
        logout()




# The rest of your Streamlit code for item checkout, return, delete, etc., would go here