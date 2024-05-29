import streamlit as st

from streamlit_navigation_bar import st_navbar

from extentions.report import show_dataframe


conn = st.connection('main_db', type='sql')
# module 4
module_4_df = conn.query('SELECT * FROM module_4_table')
# module 32
module_32_df = conn.query(f'SELECT * FROM module_32_table')
# module GE
module_ge_df = conn.query(f'SELECT * FROM module_ge_table')

default_asr = conn.query('SELECT asr_value FROM asr_value WHERE id = 1')


def highlight(s,n):
    if float(s['asr']) < n:
        if float(s['calls']) > 0:
            return ['background-color: orange'] * len(s)
        else:
            return ['background-color: white'] * len(s)
    else:
        return ['background-color: white'] * len(s)

def home_main():
    st.session_state['asr_value'] = default_asr['asr_value'][0]
    # frontend section
    st.write("Welcome!")
    column_config = {'upload_datetime':'Tanggal dan Waktu Upload', 
                        'upload_ip':'IP Perangkat'}
    
    st.subheader("Statistik Tabel Perangkat GE", anchor=False)
    with st.container(border=True):
        st.write("Tabel Terbaru")
        # dataframe with style
        view_data_ge = module_ge_df.style.apply(highlight, n=st.session_state['asr_value'], axis=1)

        show_dataframe(view_data_ge, column_config)
    st.divider()   

    st.subheader("Statistik Tabel Perangkat 32 Modul", anchor=False)
    with st.container(border=True):
        st.write("Tabel Terbaru")
        # dataframe with style
        view_data_32 = module_32_df.style.apply(highlight, n=st.session_state['asr_value'], axis=1)

        show_dataframe(view_data_32, column_config)
    st.divider()

    st.subheader("Statistik Tabel Perangkat 4 Modul", anchor=False)
    with st.container(border=True):
        st.write("Tabel Terbaru")
        # dataframe with style
        view_data_4 = module_4_df.style.apply(highlight, n=st.session_state['asr_value'], axis=1)

        show_dataframe(view_data_4, column_config)