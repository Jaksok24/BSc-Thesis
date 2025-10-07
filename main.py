import streamlit as st
from views import home, orders, routing, fleet, login, users, my_profile
from assets.sidebar_configuration import sidebar_config

st.set_page_config(page_title="TransLog", page_icon=":truck:", layout="wide")
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def main():
    if not st.session_state.logged_in:
        #Ekran logowania
        login.show()
    else:
    # Główna aplikacja
        selected = sidebar_config()

        if selected == "Strona główna":
            home.show()
        elif selected == "Planowanie tras":
            routing.show()
        elif selected == "Zlecenia":
            orders.show()
        elif selected == "Flota":
            fleet.show()
        elif selected == "Zarządzaj użytkownikami":
            users.show()
        elif selected == "Mój profil":
            my_profile.show()
        
if __name__ == "__main__":
    main()