import streamlit as st

def init_session_state():
    defaults = {
        "userID": None,
        "username": None,
        "login": None,
        "role": None,
        "logged_in": False,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val
