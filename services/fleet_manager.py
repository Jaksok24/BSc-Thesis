import streamlit as st
from services.db_connector import connect_to_db, close_db

def add_vehicle(registration_plate, vehicle_type, vehicle_payload, vehicle_status):
    add_vehicle_querry = """INSERT INTO pojazdy (rejestracja, typ, ladownosc, status) VALUES (?, ?, ?, ?)"""
    if registration_plate != "" and vehicle_payload != 0:
        conn, c = connect_to_db()

        # Sprawdzenie czy login już istnieje
        check_vehicle_query = """SELECT 1 FROM pojazdy WHERE rejestracja = ?"""
        c.execute(check_vehicle_query, (registration_plate,))
        if c.fetchone():
            st.error("Pojazd z taką tablicą rejestracyjną już istnieje")
            close_db(conn)
            return
        try:
            c.execute(add_vehicle_querry, (registration_plate, vehicle_type, vehicle_payload, vehicle_status))
            conn.commit()
            st.toast("Dodano pojazd!")
        except Exception as e:
            st.error(f"Wystąpił błąd {e}")
        finally:
            if conn:
                close_db(conn)
    else:
        st.error("Wprowadź wszystkie dane")

def edit_vehicle():
    #To będzie funkcja do edytowania zlecen
    pass
