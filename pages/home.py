# home.py
import streamlit as st

#if not logged in dont show anything
if not st.session_state.get('logged_in', False):
    st.error("You are not logged in.")
    st.stop()
    
st.title("Home Page")
st.write("Welcome to the Lab Equipment Inventory System!")
# Add more content for the Home Page here
