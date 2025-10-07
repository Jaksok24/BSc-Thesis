import streamlit as st

def show():
    left, right = st.columns(2)
    with left:
        start_location = st.text_input("Początkowa lokalizacja", placeholder="np. Warszawa")
    with right:
        end_location = st.text_input("Końcowa lokalizacja", placeholder="np. Kraków")
    with st.container(border=True):
        st.map()
    st.write("Po wpisaniu dwóch lokalizacji pokaze się trasa i jej długość w km i h")
