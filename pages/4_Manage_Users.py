#manage_users.py
import datetime
import streamlit as st
import psycopg2
import pandas as pd

#if not logged in dont show anything
if not st.session_state.get('logged_in', False):
    st.error("You are not logged in.")
    st.stop()

def logout():
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()
if st.sidebar.button("Logout"):
    logout()

user_id = st.session_state.get('user_id') #accessing gloabal userID variable from login
user_name = st.session_state.get('user_name')
user_role = st.session_state.get('user_role')

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

def display_user_table():
    #function to display the equipment table
    with connect_to_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT Users.users_id, Users.users_name, UsersProject.project_name, UsersProject.sponsor, UsersProject.is_team_lead FROM Users, UsersProject WHERE Users.users_id=UsersProject.users_id;")
            raw_data = cur.fetchall()
            column_names = ["User ID", "User Name", "Project Name", "Sponsor", "Is Team Lead"]
    data_frame = pd.DataFrame(raw_data, columns=column_names)
    st.dataframe(data_frame)  # Or st.table(data_frame)

def display_user_deletion_form():
    st.subheader("Delete User:")
    with connect_to_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT users_id FROM Users;")
            user_ids = [row[0] for row in cur.fetchall()]
    remove_user_id = st.selectbox("User To Delete:", user_ids)
    if st.button("Delete"):
        with connect_to_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(DISTINCT(Equipment.equip_id)) FROM Equipment, Transaction WHERE Equipment.equip_id=Transaction.equipment_items[1] AND Transaction.users_id=%s AND Transaction.actual_return_date=%s;", (remove_user_id, datetime.date(datetime.MINYEAR, 1, 1),))
                equipment_count = cur.fetchall()
        if equipment_count[0][0] == 0:
            with connect_to_db() as conn:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM UsersProject WHERE users_id=%s;", (remove_user_id,))
                    cur.execute("DELETE FROM Users WHERE users_id=%s;", (remove_user_id,))
            st.success("User deleted successfully")
        else:
            st.error("User has currently checked out items.")
        

def display_user_addition_form():
    st.subheader("Add User:")
    new_user_id = st.text_area("Provide a User ID:")
    new_user_name = st.text_area("Provide a User Name:")
    with connect_to_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT DISTINCT(project_name) FROM Project;")
            project_names = [row[0] for row in cur.fetchall()]

    project_to_add_to = st.selectbox("Add To Project:", project_names)

    with connect_to_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT DISTINCT(sponsor) FROM Project WHERE project_name=%s;", (project_to_add_to,))
            sponsor_list = [row[0] for row in cur.fetchall()]

    sponsor = st.selectbox("With Sponsor:", sponsor_list)

    is_team_lead = st.selectbox("Is a Team Lead:", ['t', 'f'])
    
    if st.button("Add"):
        with connect_to_db() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO Users (users_id, users_name) VALUES (%s, %s);", (new_user_id, new_user_name,))
                cur.execute("INSERT INTO UsersProject (users_id, project_name, sponsor, is_team_lead) VALUES (%s, %s, %s, %s);", (new_user_id, project_to_add_to, sponsor, is_team_lead,))
        st.success("User added succesfully")

if user_role == 'admin':
    st.title("Manage Users")
    display_user_table()
    display_user_addition_form()
    display_user_deletion_form()
    
else:
    st.error("You do not have access to this page.")