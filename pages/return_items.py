# return_items.py
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

st.title("Return Items")
st.write("This page allows you to return borrowed items.")


#TO DO: Add functionalities to list borrowed items and manage returns
