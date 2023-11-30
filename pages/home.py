# home.py
import streamlit as st

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

st.title("Home Page")
st.write("Welcome to the Lab Equipment Inventory System!")


# TO DO: Add more content for the Home Page here
