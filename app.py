import streamlit as st
st.set_page_config(initial_sidebar_state="collapsed", layout="wide")

from datetime import timedelta
from streamlit_navigation_bar import st_navbar
import pages as pg
import schedule, time


page = st_navbar(["Dashboard","Statistik GE", "Statistik 4 Modul", "Statistik 32 Modul", "Manajemen Perangkat"],
                 options={'show_menu':False, 'show_sidebar':False})

conn = st.connection('main_db', type='sql', ttl=timedelta(minutes=1))

def clear_cache():
    st.cache_data.clear()
    st.cache_resource.clear()
    print("cache cleared")
    st.rerun()

def get_asr(conn):
    default_asr = conn.query('SELECT asr_value FROM asr_value WHERE id = 1')
    st.session_state['asr_value'] = default_asr['asr_value'][0]

def main():
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

schedule.every(1).minutes.do(clear_cache)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    get_asr(conn)
    main()
