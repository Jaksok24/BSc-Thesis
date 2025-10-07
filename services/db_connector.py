import sqlite3
import streamlit as st

def connect_to_db():
    try:
        conn = sqlite3.connect("storage/db.sqlite3", check_same_thread=False)
        c = conn.cursor()
        return conn, c
    except Exception as e:
        st.error(f"Błąd podczas łączenia z bazą danych: {e}")

def close_db(conn):
    conn.close()
