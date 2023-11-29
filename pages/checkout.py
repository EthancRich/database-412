# checkout.py
import streamlit as st

#if not logged in dont show anything
if not st.session_state.get('logged_in', False):
    st.error("You are not logged in.")
    st.stop()


st.title("Check Out Items")
st.write("Here you can check out items from the inventory.")
# Add forms, tables, or other elements to manage item checkout
