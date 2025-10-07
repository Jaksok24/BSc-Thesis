import hashlib
import streamlit as st
from services.db_connector import connect_to_db, close_db
from services.session import init_session_state
from models.classes import User

init_session_state()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_user(login_input, password_input):
    for key in ["userID", "username", "login", "role", "logged_in"]:
        if key not in st.session_state:
            st.session_state[key] = None

    try:
        check_user_querry = """SELECT uID, nazwa_uzytkownika, imie_nazwisko, rola, haslo FROM uzytkownicy WHERE nazwa_uzytkownika = ?"""
        conn, c = connect_to_db()
        c.execute(check_user_querry, (login_input,))
        result = c.fetchone()

        if result:
            user = User(uID=result[0], username=result[2], login=result[1], role=result[3], password=result[4])
            if user.password == hash_password(password_input):
                st.session_state.userID = user.uID
                st.session_state.username = user.username
                st.session_state.login = user.login
                st.session_state.role = user.role
                st.session_state.logged_in = True
                st.success("Zalogowano pomyślnie!")
            else:
                st.error("Nieprawidłowe hasło.")
        else:
            st.error("Nie znaleziono użytkownika")
    except Exception as e:
        st.error(f"Wystąpił błąd podczas logowania {e}")
    finally:
        if conn:
            close_db(conn)

def logout_user():
    for key in ["userID", "username", "login", "role"]:
        st.session_state[key] = None
    st.session_state["logged_in"] = False
