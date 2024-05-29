import streamlit as st
import pandas as pd

from io import BytesIO
from sqlalchemy.sql import text


# connection to sqlite
conn = st.connection('main_db', type='sql')


# get the latest data of database
def clear_cache():
    st.cache_data.clear()
    st.cache_resource.clear()
    st.rerun()

# highlight dataframe based on input
def highlight(s,n):
    if float(s['asr']) < n:
        if float(s['calls']) > 0:
            return ['background-color: orange'] * len(s)
        else:
            return ['background-color: white'] * len(s)
    else:
        return ['background-color: white'] * len(s)

def show_dataframe(df:pd.DataFrame, column_config):
    return st.dataframe(df, use_container_width=True, 
                 hide_index=True, 
                 column_config=column_config)

def download_excel(filename:str, df:pd.DataFrame):
    buffer = BytesIO()
    with pd.ExcelWriter(buffer) as writer:
        df.to_excel(writer, index=False)
    st.download_button(label="Download", 
                       type='primary', 
                       data=buffer.getvalue(), 
                       file_name=filename, 
                       mime='application/vnd.ms-excel',
                       key="download_excel_key")

def delete_table(tablename:str, db_connection):
    clear_btn = st.button("Hapus Tabel", type='secondary', key="clear_btn_key")
    if clear_btn:
        with db_connection.session as s:
            s.execute(text(f'DELETE FROM {tablename}'))
            s.commit()
        clear_cache()

def update_asr(db_connection, update_value):
    st.session_state['asr_value'] = update_value
    with db_connection.session as s:
        s.execute(text(f'UPDATE asr_value SET asr_value = {update_value} WHERE id = 1'))
        s.commit()
    clear_cache()

def report_section(df:pd.DataFrame, module:str):
    column_config = {'upload_datetime':'Tanggal dan Waktu Upload', 
                     'upload_ip':'IP Perangkat'}
    
    with st.container(border=True):
        st.write("Tabel Terbaru")
        input1, input2, input3 = st.columns(3)
        with input1:
            asr_input = st.number_input('Input ASR', min_value=0, 
                                        max_value=100, value=st.session_state['asr_value'], step=1, 
                                        key="asr_input_key")
            if asr_input != st.session_state['asr_value']:
                update_asr(conn, asr_input)

            filter_data = st.checkbox('Tampilkan Data dibawah ASR', key="checkbox_key")
        # dataframe with style
        if filter_data:
            # change TEXT data column to numeric for filter
            view_data = df[df['asr'].apply(pd.to_numeric) < st.session_state['asr_value']]
        else:
            view_data = df.style.apply(highlight, n=asr_input, axis=1)

        show_dataframe(view_data, column_config)
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            download_excel(f'report_{module}.xlsx', view_data)     
        with col2:
            delete_table(f'{module}_table', conn)
