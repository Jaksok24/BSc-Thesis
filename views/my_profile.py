import streamlit as st
from streamlit_option_menu import option_menu

def profile_tabs():
    selected = option_menu(
        menu_title=None,
        options=["Dane osobowe", "Zmiana hasła"],
        icons=["cart-plus","pencil-square"],
        orientation="horizontal"
    )
    return selected

def show():
    selected = profile_tabs()
    
    if selected == "Dane osobowe":
        with st.container(border=True):
            st.markdown("### 👤 Profil użytkownika")
            st.markdown(
                f"""
                **Imię i nazwisko:** {st.session_state['username']}  
                **Login:** {st.session_state['login']}  
                **Rola:** {st.session_state['role']}
                """
            )

    if selected == "Zmiana hasła":
        st.header("Zmiana hasła", anchor=False)
        with st.form(key="change_password_form", clear_on_submit=True, border=True):
            old_password = st.text_input("Stare hasło", type="password")
            new_password = st.text_input("Nowe hasło", type="password")
            confirm_password = st.text_input("Potwierdź nowe hasło", type="password")
            if st.form_submit_button("Zmień hasło"):
                
                #Dodać logikę do zmiany hasła!!!
                
                st.toast("Hasło zostało zaktualizowane!")
                pass