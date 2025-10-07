import streamlit as st
from datetime import date
from services.db_connector import *
from models.classes import Order
from services.order_manager import update_order

def show():
    status_options = ["Oczekujące", "W drodze", "Zakończone"]
    
    st.header(f"Zlecenia na dzień {date.today().strftime("%d.%m.%Y")}", anchor=False)
    st.divider()
    
    conn, c = connect_to_db()
    c.execute(f"SELECT * FROM zlecenia WHERE data_zaladunku = '{date.today().strftime("%Y-%m-%d")}'")
    orders = c.fetchall()
    orders_list = []
    if orders:
        for order in orders:
            order_obj = Order(order[0], order[1], order[2], order[3], order[4], order[5], order[6], order[7], order[8])
            orders_list.append(order_obj)
            
            with st.popover(f"Klient: {order_obj.customer} | Kierowca: {order_obj.driver} | Pojazd: {order_obj.vehicle}", use_container_width=True):
                left, right = st.columns(2)
                with left:
                    st.write(f"Data zaladunku: {order_obj.load_date}")
                    st.write(f"Miejsce zaladunku: {order_obj.load_location}")
                with right:
                    st.write(f"Data rozładunku: {order_obj.unload_date}")
                    st.write(f"Miejsce rozładunku: {order_obj.unload_location}")
                status = st.selectbox("Status", options=status_options)
                if status != order_obj.status:
                    update_order(order_obj.oID, status)
                    st.toast("Zaktualizowano status!")
                    
    else:
        st.write("Brak zleceń na dzisiaj")
    close_db(conn)