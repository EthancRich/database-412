# return_items.py
import streamlit as st

#if not logged in dont show anything
if not st.session_state.get('logged_in', False):
    st.error("You are not logged in.")
    st.stop()
    
st.title("Return Items")
st.write("This page allows you to return borrowed items.")
# Add functionalities to list borrowed items and manage returns
