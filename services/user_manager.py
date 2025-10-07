import streamlit as st
from services.db_connector import connect_to_db, close_db
from services.auth import hash_password

def add_user(username, user_login, user_role, user_password, confirm_user_password):
    add_user_querry = """INSERT INTO uzytkownicy (nazwa_uzytkownika, imie_nazwisko, rola, haslo) VALUES (?, ?, ?, ?)"""
    if username != "" and user_login != "":
        if hash_password(user_password) == hash_password(confirm_user_password):
            conn, c = connect_to_db()

            # Sprawdzenie czy login już istnieje
            check_user_query = """SELECT 1 FROM uzytkownicy WHERE nazwa_uzytkownika = ?"""
            c.execute(check_user_query, (user_login,))
            if c.fetchone():
                st.error("Użytkownik z takim loginem już istnieje")
                close_db(conn)
                return

            try:
                c.execute(add_user_querry, (user_login, username, user_role, hash_password(user_password)))
                conn.commit()
                st.toast("Dodano użytkonika!")
            except Exception as e:
                st.error(f"Wystąpił błąd {e}")
            finally:
                if conn:
                    close_db(conn)
        else:
            st.error("Hasła nie są identyczne")
    else:
        st.error("Wprowadź wszystkie dane")

def edit_user(uID, username, user_login, user_role):
    edit_user_querry = """UPDATE uzytkownicy SET imie_nazwisko = ?, nazwa_uzytkownika = ?, rola = ? WHERE uID = ?"""
    conn, c = connect_to_db()
    try:
        c.execute(edit_user_querry, (username, user_login, user_role, uID))
        conn.commit()
    except Exception as e:
        st.error(f"Wystąpił błąd {e}")
    finally:
        if conn:
            close_db(conn)
