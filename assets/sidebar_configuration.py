import streamlit as st
from streamlit_option_menu import option_menu
from services.session import init_session_state
from services.auth import logout_user

init_session_state()

def sidebar_config():
    with st.sidebar:
        st.header(f"Witaj, {st.session_state['username']}!", anchor=False, divider=True)
        if st.session_state['role'] == "Manager" or st.session_state['role'] == "Admin":
            selected = option_menu("Menu",
                ["Strona główna", "Planowanie tras", "Zlecenia", "Flota", "Zarządzaj użytkownikami"],
                icons=["house","signpost-2","briefcase","bus-front","people"],
                menu_icon="truck",
                default_index=0
            )
        else:
            selected = option_menu("Menu",
                ["Strona główna", "Planowanie tras", "Mój profil"],
                icons=["house","signpost-2", "person"],
                menu_icon="truck",
                default_index=0
            )
        rerun_button = st.button("Odśwież", use_container_width=True)
        if rerun_button:
            st.rerun()
        logout_button = st.button("Wyloguj się", use_container_width=True, type="primary")
        if logout_button:
            logout_user()
            st.rerun()
    return selected
