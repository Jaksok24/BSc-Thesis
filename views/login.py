import streamlit as st
from services.auth import check_user
from services.db_connector import connect_to_db, close_db

def show():
    left, middle, right = st.columns(3)
    with middle:
        st.header("Zaloguj się", anchor=False)
        with st.form(key="logging_form", clear_on_submit=True, border=True):
            login_input = st.text_input("Podaj login")
            password_input = st.text_input("Podaj hasło", type="password")
            login_button = st.form_submit_button("Zaloguj się", use_container_width=True)
            if login_button:
                check_user(login_input, password_input)
                st.rerun()