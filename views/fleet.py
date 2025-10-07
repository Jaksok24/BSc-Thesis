import streamlit as st
from streamlit_option_menu import option_menu
from services.fleet_manager import *
from models.classes import Vehicle

def fleet_tabs():
    selected = option_menu(
        menu_title=None,
        options=["Dodaj pojazd", "Zarządzaj pojazdami"],
        icons=["truck-flatbed","tools"],
        orientation="horizontal"
    )
    return selected

def show():
    selected = fleet_tabs()
    if selected == "Dodaj pojazd":
        with st.form(key="add_vehicle_form", clear_on_submit=True, border=True):
            left, right = st.columns(2)
            with left:
                registration_plate = st.text_input("Tablica rejestracyjna")
                vehicle_type = st.selectbox("Typ pojazdu", options=["Samochód ciężarowy", "Samochód dostawczy"])
            with right:
                vehicle_capacity = st.number_input("Ładowność", min_value=0.0, max_value=40.0 if vehicle_type == "Samochód ciężarowy" else 2.5, step=0.1)
                vehicle_status = st.selectbox("Status", options=["Dostępny", "W trasie", "Serwis"])
            add_vehicle_button = st.form_submit_button("Dodaj", use_container_width=True)
            if add_vehicle_button:
                try:
                    add_vehicle(registration_plate, vehicle_type, vehicle_capacity, vehicle_status)
                except:
                    st.warning("Wystąpił błąd!")

    if selected == "Zarządzaj pojazdami":
        conn, c = connect_to_db()
        c.execute("SELECT * FROM pojazdy")
        vehicles = c.fetchall()
        close_db(conn)
        
        vehicle_list = []
        for vehicle in vehicles:
            vehicle_list.append(Vehicle(vehicle[0], vehicle[1], vehicle[2], vehicle[3], vehicle[4]))
        for vehicle in vehicle_list:
            with st.popover(f"Pojazd nr {vehicle.vID}", use_container_width=True):
                with st.form(key=f"add_vehicle_form_{vehicle.vID}", clear_on_submit=True, border=True):
                    left, right = st.columns(2)
                    with left:
                        registration_plate = st.text_input("Tablica rejestracyjna", value=vehicle.registration, key=f"registration_plate_{vehicle.vID}")
                        vehicle_type = st.selectbox("Typ pojazdu", options=["Samochód ciężarowy", "Samochód dostawczy"], index=0 if vehicle.type == "Samochód ciężarowy" else 1, key=f"vehicle_type_{vehicle.vID}")
                    with right:
                        vehicle_capacity = st.number_input("Ładowność", min_value=0.0, max_value=40.0 if vehicle_type == "Samochód ciężarowy" else 2.5, step=0.1, value=float(vehicle.load_capacity), key=f"vehicle_payload_{vehicle.vID}")
                        vehicle_status = st.selectbox("Status", options=["Dostępny", "W trasie", "Serwis"], index=0 if vehicle.status == "Dostępny" else 1 if vehicle.status == "W trasie" else 2, key=f"vehicle_status_{vehicle.vID}")
                    edit_vehicle_button = st.form_submit_button("Zaktualizuj", use_container_width=True)
                    if edit_vehicle_button:
                        try:
                            st.toast("Zaktualizowano pojazd!")
                            edit_vehicle(vehicle.vID, registration_plate, vehicle_type, vehicle_capacity, vehicle_status)
                        except:
                            st.warning("Wystąpił błąd!")
