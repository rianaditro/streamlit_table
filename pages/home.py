import streamlit as st

from streamlit_navigation_bar import st_navbar

from extentions.report import show_dataframe


conn = st.connection('main_db', type='sql')
# module 4
module_4_df = conn.query('SELECT * FROM module_4_table')
# module 32
module_32_df = conn.query(f'SELECT * FROM module_32_table')

def highlight(s,n):
    if float(s['asr']) <= n:
        return ['background-color: orange'] * len(s)
    else:
        return ['background-color: white'] * len(s)

def home_main():
    # frontend section
    st.write("welcome,")
    st.subheader("Statistik Tabel Perangkat 32 Modul", anchor=False)
    column_config = {'upload_datetime':'Tanggal dan Waktu Upload', 
                        'upload_ip':'IP Perangkat'}
        
    with st.container(border=True):
        st.write("Tabel Terbaru")
        input1, input2, input3 = st.columns(3)
        with input1:
            asr_input = st.number_input('Input ASR', min_value=0, 
                                        max_value=100, value=30, step=1, 
                                        key="asr_home_key")
        # dataframe with style
        view_data_32 = module_32_df.style.apply(highlight, n=asr_input, axis=1)

        show_dataframe(view_data_32, column_config)
    st.divider()
    st.subheader("Statistik Tabel Perangkat 4 Modul", anchor=False)
    with st.container(border=True):
        st.write("Tabel Terbaru")
        # dataframe with style
        view_data_4 = module_4_df.style.apply(highlight, n=asr_input, axis=1)

        show_dataframe(view_data_4, column_config)