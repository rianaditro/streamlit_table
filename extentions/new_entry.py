import streamlit as st
import pandas as pd

from io import StringIO
from datetime import datetime
from sqlalchemy.sql import text

from extentions.converter import extract_module_4, extract_module_32


def clear_cache():
    st.cache_data.clear()
    st.cache_resource.clear()
    st.rerun()

def preview_upload_file(upload_file, module):
    txt = StringIO(upload_file.getvalue().decode("utf-8")).readlines()
    if module == 'module_4':
        preview_df = extract_module_4(txt)
    elif module == 'module_32':
        preview_df = extract_module_32(txt)
    preview_df = pd.DataFrame(preview_df)
    return preview_df

def append_history(conn, data):
    with conn.session as s:
        s.execute(text(f'''INSERT INTO history_upload (upload_id, upload_datetime, ip_address) VALUES ("{data['upload_id']}", "{data['upload_datetime']}", "{data['upload_ip']}")'''))
        s.commit()
               
def append_table(conn, df:pd.DataFrame, tablename):
    cursor = conn.connect()
    df.to_sql(tablename, cursor, if_exists='append', index=False)
    if "file_uploader_key" in st.session_state:
        st.session_state["file_uploader_key"] += 1
        del st.session_state[(st.session_state["file_uploader_key"]-1)]
    clear_cache()

def upload_data(conn, dataframe, ip_address, module):
    upload_datetime = datetime.now()
    upload_id = upload_datetime.strftime("%Y%m%d%H")+'_ID'
    upload_ip = ip_address
    dataframe = dataframe.assign(upload_id=upload_id,upload_datetime=upload_datetime,upload_ip=upload_ip)
    
    # re-order columns
    if module == 'module_4':
        dataframe = dataframe[['upload_id','upload_datetime','upload_ip','module', '-', 'reset', 'minutes', 'hms', 'calls', 'reject', 'failed', 'coffs', 'smses','asr']]
    elif module == 'module_32':
        dataframe = dataframe[['upload_id','upload_datetime','upload_ip','module', 'sim', 'net', 'minutes', 'hms', 'calls', 'reject', 'failed', 'coffs', 'smses','asr']]
    elif module == 'module_ge':
        dataframe = dataframe[['upload_id','upload_datetime','upload_ip','mobile_port', 'port_status', 'signal_strength', 'call_duration', 'dialed_calls', 'successfull_calls', 'asr', 'acd', 'allocated_ammount', 'consumed_amount']]
    
    # add history data into database
    history_data = {'upload_id':upload_id, 'upload_datetime':upload_datetime, 'upload_ip':upload_ip}
    append_history(conn, history_data)
    # append to database
    append_table(conn, dataframe, f'{module}_table')

def entry_section(conn, module):
    # validate module and database
    if module == 'module_4':
        tipe_perangkat = 'Perangkat 4 Modul'
    elif module == 'module_32':
        tipe_perangkat = 'Perangkat 32 Modul'
    elif module == 'module_ge':
        tipe_perangkat = 'Perangkat GE'
    else:
        tipe_perangkat = '------------------'

    # get list of selectbox
    perangkat_df = conn.query(f'SELECT * FROM perangkat_table WHERE tipe_perangkat = "{tipe_perangkat}"')
    if len(perangkat_df) == 0:
        daftar_nama_perangkat = ['------------------']
        daftar_ip_address = ['------------------']
    else:
        daftar_nama_perangkat = perangkat_df['nama_perangkat'].tolist()
        daftar_ip_address = perangkat_df['ip_address'].tolist()

    # set key for widget upload file
    if "file_uploader_key" not in st.session_state:
        st.session_state["file_uploader_key"] = 0

    st.subheader("Tambah File", anchor=False)
    col1, col2, col3 = st.columns(3)
    with col1:
        nama_perangkat_selected = st.selectbox('Nama Perangkat', options=daftar_nama_perangkat, placeholder='Pilih Perangkat', key='nama_perangkat_key')
        try:
            index = daftar_nama_perangkat.index(nama_perangkat_selected)
        except ValueError:
            index = 0
    with col2:
        ip_address_selected = st.text_input("IP Address", value=daftar_ip_address[index],disabled=True, key='ip_address_key')
    with col3:
        tipe_perangkat_selected = st.text_input('Tipe Perangkat', value=tipe_perangkat, disabled=True, key='tipe_perangkat_key')

    upload = st.file_uploader('Pilih File', type='txt', accept_multiple_files=False, key=st.session_state["file_uploader_key"])

    if upload:
        preview_df = preview_upload_file(upload, module)
        st.write("Preview")
        st.dataframe(preview_df, use_container_width=True, hide_index=True)
        
        submit_btn = st.button("Tambah ke Database", type='primary', key="submit_btn")
        if submit_btn:
            # add additional data
            upload_data(conn, preview_df, ip_address_selected, module)