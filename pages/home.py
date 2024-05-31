import streamlit as st
import pandas as pd

from datetime import timedelta
from sqlalchemy import text


def clear_cache():
    st.cache_data.clear()
    st.cache_resource.clear()
    st.rerun()

def update_asr(db_connection, update_value):
    st.session_state['asr_value'] = update_value
    with db_connection.session as s:
        s.execute(text(f'UPDATE asr_value SET asr_value = {update_value} WHERE id = 1'))
        s.commit()
    clear_cache()

def get_data(conn):
# module 4
    module_4_df = conn.query('SELECT m.upload_id, m.upload_datetime, p.nama_perangkat, m.upload_ip, p.tipe_perangkat, m.module, m.hms, m.calls, m.asr FROM module_4_table AS m JOIN perangkat_table AS p ON m.upload_ip = p.ip_address WHERE p.tipe_perangkat = "Perangkat 4 Modul" ORDER BY m.upload_datetime DESC')
    module_4_df.rename(columns={'module':'module/mobile_port', 'hms':'call_duration', 'calls':'successfull_calls', 'asr':'ASR(%)'}, inplace=True)
    # module 32
    module_32_df = conn.query('SELECT m.upload_id, m.upload_datetime, p.nama_perangkat, m.upload_ip, p.tipe_perangkat, m.module, m.hms, m.calls, m.asr FROM module_32_table AS m JOIN perangkat_table AS p ON m.upload_ip = p.ip_address WHERE p.tipe_perangkat = "Perangkat 32 Modul" ORDER BY m.upload_datetime DESC')
    module_32_df.rename(columns={'module':'module/mobile_port', 'hms':'call_duration', 'calls':'successfull_calls', 'asr':'ASR(%)'}, inplace=True)
    # module GE
    module_ge_df = conn.query('SELECT m.upload_id, m.upload_datetime, p.nama_perangkat, m.upload_ip, p.tipe_perangkat, m.mobile_port, m.call_duration, m.successfull_calls, m.asr FROM module_ge_table AS m JOIN perangkat_table AS p ON m.upload_ip = p.ip_address WHERE p.tipe_perangkat = "Perangkat GE" ORDER BY m.upload_datetime DESC')
    module_ge_df.rename(columns={'mobile_port':'module/mobile_port', 'asr':'ASR(%)'}, inplace=True)

    data = pd.concat([module_4_df, module_32_df, module_ge_df], ignore_index=True)
    return data

def highlight(s,n):
    if float(s['ASR(%)']) < n:
        if float(s['successfull_calls']) > 0:
            return ['background-color: orange'] * len(s)
        else:
            return ['background-color: white'] * len(s)
    else:
        return ['background-color: white'] * len(s)

def home_main(conn):
    data = get_data(conn)
    # frontend section
    st.write("Welcome!")
    
    st.subheader("Statistik Tabel Gabungan", anchor=False)
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
            view_data = data[data['ASR(%)'].apply(pd.to_numeric) < st.session_state['asr_value']]
            # remove data with 0 calls
            view_data = view_data[view_data['successfull_calls'] != '0']
        else:
            view_data = data.style.apply(highlight, n=asr_input, axis=1)

        st.dataframe(view_data)
