import streamlit as st
from streamlit_option_menu import option_menu
from services.user_manager import *
from services.data_loader import get_data_to_dataframe
from models.classes import User

def user_tabs():
    selected = option_menu(
        menu_title=None,
        options=["Dodaj użytkonika", "Zarządzaj użytkownikami"],
        icons=["person-add","person-gear"],
        orientation="horizontal"
    )
    return selected

def show():
    selected = user_tabs()

    if selected == "Dodaj użytkonika":
        with st.form(key="add_user_form", clear_on_submit=True, border=True):
            username = st.text_input("Imię i nazwisko")
            left, right = st.columns(2)
            with left:
                user_login = st.text_input("Login")
            with right:
                user_role = st.selectbox("Rola", options=["Kierowca", "Manager"])
            user_password = st.text_input("Hasło", type="password")
            confirm_user_password = st.text_input("Potwierdź hasło", type="password")
            add_user_button = st.form_submit_button("Dodaj", use_container_width=True)
            if add_user_button:
                add_user(username, user_login, user_role, user_password, confirm_user_password)

    if selected == "Zarządzaj użytkownikami":
        conn, c = connect_to_db()
        c.execute("SELECT * FROM uzytkownicy")
        users = c.fetchall()
        close_db(conn)
        users_list = []
        for user in users:
            users_list.append(User(user[0], user[1], user[2], user[3], user[4]))
        for user in users_list:
            if user.role != "Admin":
                with st.popover(f"{user.username} | {user.role}", use_container_width=True):
                    with st.form(key=f"edit_user_form_{user.uID}", clear_on_submit=True, border=True):
                        username = st.text_input("Imię i nazwisko", value=user.username, key=f"username_{user.uID}")
                        left, right = st.columns(2)
                        with left:
                            user_login = st.text_input("Login", value=user.login, key=f"login_{user.uID}")
                        with right:
                            user_role = st.selectbox("Rola", options=["Kierowca", "Manager"], index=0 if user.role == "Kierowca" else 1, key=f"role_{user.uID}")
                        edit_user_button = st.form_submit_button("Zaktualizuj dane", use_container_width=True)
                        if edit_user_button:
                            try:
                                edit_user(user.uID, username, user_login, user_role)
                                st.toast("Zaktualizowano dane użytkownika!")
                            except Exception as e:
                                st.warning(f"Wystąpił błąd! {e}")