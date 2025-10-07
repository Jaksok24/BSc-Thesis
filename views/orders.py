import streamlit as st
from datetime import datetime
from streamlit_option_menu import option_menu
from services.order_manager import *
from services.db_connector import *
from models.classes import Order

def order_tabs():
    selected = option_menu(
        menu_title=None,
        options=["Dodaj zlecenie", "Edytuj zlecenie"],
        icons=["cart-plus","pencil-square"],
        orientation="horizontal"
    )
    return selected
            
def show():
    selected = order_tabs()
    drivers = get_drivers()
    trucks =  get_trucks()
    
    vehicle_options = [truck[0] for truck in trucks]
    driver_options = [driver[0] for driver in drivers]
    status_options = ["Oczekujące", "W drodze", "Zakończone"]
    
    if selected == "Dodaj zlecenie":
        with st.form(key="add_order_form", clear_on_submit=True, border=True):
            left, right = st.columns(2)
            with left:
                customer = st.text_input("Klient")
                vehicle = st.selectbox("Pojazd", options=vehicle_options)
                driver = st.selectbox("Kierowca", options=driver_options)
                status = st.selectbox("Status", options=status_options)
            with right:
                loading_location = st.text_input("Miejsce załadunku")
                unloading_location = st.text_input("Miejsce rozładunku")
                loading_data = st.date_input("Data załadunku")
                unloading_data = st.date_input("Data rozładunku")
            confirm_adding_button = st.form_submit_button("Dodaj", use_container_width=True)
            if confirm_adding_button:
                try:
                    add_order(customer, vehicle, driver, status, loading_location, unloading_location, loading_data, unloading_data)
                    st.toast("Dodano zlecenie!")
                except Exception as e:
                    st.warning(f"Wystąpił błąd! {e}")
        
    if selected == "Edytuj zlecenie":
        conn, c = connect_to_db()
        c.execute("SELECT * FROM zlecenia")
        orders = c.fetchall()
        close_db(conn)
        
        orders_list = []
        for order in orders:
            orders_list.append(Order(order[0], order[1], order[2], order[3], order[4], order[5], order[6], order[7], order[8]))
            
        for order in orders_list:
            # Szukanie indeksu bieżącej wartości w opcjach
            vehicle_index = vehicle_options.index(order.vehicle) if order.vehicle in vehicle_options else 0
            driver_index = driver_options.index(order.driver) if order.driver in driver_options else 0
            status_index = status_options.index(order.status) if order.status in status_options else 0
            
            load_date = datetime.strptime(order.load_date, "%Y-%m-%d").date()
            unload_date = datetime.strptime(order.unload_date, "%Y-%m-%d").date()
            
            with st.popover(f"Zlecenie nr {order.oID}", use_container_width=True):
                with st.form(key=f"add_order_form_{order.oID}", clear_on_submit=True, border=True):
                    left, right = st.columns(2)
                    with left:
                        customer = st.text_input("Klient", value=order.customer, key=f"customer_{order.oID}")
                        vehicle = st.selectbox("Pojazd", options=vehicle_options, index=vehicle_index, key=f"vehicle_{order.oID}")
                        driver = st.selectbox("Kierowca", options=driver_options, index=driver_index, key=f"driver_{order.oID}")
                        status = st.selectbox("Status", options=status_options, index=status_index, key=f"status_{order.oID}")
                    with right:
                        loading_location = st.text_input("Miejsce załadunku", value=order.load_location, key=f"loading_location_{order.oID}")
                        unloading_location = st.text_input("Miejsce rozładunku", value=order.unload_location, key=f"unloading_location_{order.oID}")
                        loading_data = st.date_input("Data załadunku", value=load_date, key=f"load_data_{order.oID}")
                        unloading_data = st.date_input("Data rozładunku", value=unload_date, key=f"unload_data_{order.oID}")
                    edit_order_button = st.form_submit_button("Zapisz", use_container_width=True)
                    if edit_order_button:
                        try:
                            edit_order(order.oID, customer, vehicle, driver, status, loading_location, unloading_location, loading_data, unloading_data)
                            st.toast("Zaktualizowano zlecenie!")
                        except Exception as e:
                            st.warning(f"Wystąpił błąd! {e}")