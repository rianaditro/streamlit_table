import streamlit as st
from streamlit_navigation_bar import st_navbar
import pages as pg

st.set_page_config(initial_sidebar_state="collapsed", layout="wide")

page = st_navbar(["Dashboard", "Statistik 4 Modul", "Statistik 32 Modul", "Manajemen Perangkat"],
                 options={'show_menu':False, 'show_sidebar':False})
if page == "Dashboard":
    pg.home_main()
elif page == "Statistik 4 Modul":
    pg.module_4_main()
elif page == "Statistik 32 Modul":
    pg.module_32_main()
elif page == "Manajemen Perangkat":
    pg.perangkat_main()