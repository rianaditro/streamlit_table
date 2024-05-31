import streamlit as st
st.set_page_config(initial_sidebar_state="collapsed", layout="wide")

from streamlit_navigation_bar import st_navbar
import pages as pg


page = st_navbar(["Dashboard","Statistik GE", "Statistik 4 Modul", "Statistik 32 Modul", "Manajemen Perangkat"],
                 options={'show_menu':False, 'show_sidebar':False})

conn = st.connection('main_db', type='sql')

def get_asr(conn):
    default_asr = conn.query('SELECT asr_value FROM asr_value WHERE id = 1')
    st.session_state['asr_value'] = default_asr['asr_value'][0]

get_asr(conn)

if page == "Dashboard":
    pg.home_main(conn)
elif page == "Statistik GE":
    pg.ge_main_module(conn)
elif page == "Statistik 4 Modul":
    pg.module_4_main(conn)
elif page == "Statistik 32 Modul":
    pg.module_32_main(conn)
elif page == "Manajemen Perangkat":
    pg.perangkat_main(conn)