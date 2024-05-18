import streamlit as st
import pandas as pd

from io import StringIO
from datetime import datetime

from extentions.converter import extract_module_4, extract_module_32


conn = st.connection('main_db', type='sql')
cursor = conn.connect()


def clear_cache():
    st.cache_data.clear()
    st.cache_resource.clear()
    st.rerun()

def preview_upload_file(upload_file, module):
    txt = StringIO(upload_file.getvalue().decode("utf-8")).readlines()
    if module == 'module_4':
        preview_df = extract_module_4(txt)
        preview_df = pd.DataFrame(preview_df)
    elif module == 'module_32':
        preview_df = extract_module_32(txt)
    return preview_df
               
def append_table(df:pd.DataFrame, tablename):
    df.to_sql(tablename, cursor, if_exists='replace', index=False)
    st.session_state["file_uploader_key"] += 1
    del st.session_state[(st.session_state["file_uploader_key"]-1)]
    clear_cache()

def entry_section(conn, module):
    # get list of selectbox
    perangkat_df = conn.query('SELECT * FROM ip_address')
    daftar_perangkat = perangkat_df['nama_perangkat'].tolist()

    # set key for widget upload file
    if "file_uploader_key" not in st.session_state:
        st.session_state["file_uploader_key"] = 0

    st.subheader("Tambah File", anchor=False)
    perangkat = st.selectbox('Pilih Perangkat', options=daftar_perangkat, placeholder='Pilih Perangkat')
    upload = st.file_uploader('Pilih File', type='txt', accept_multiple_files=False, key=st.session_state["file_uploader_key"])

    if upload:
        preview_df = preview_upload_file(upload, module)
        st.write("Preview")
        st.dataframe(preview_df, use_container_width=True, hide_index=True)
        
        submit_btn = st.button("Tambah ke Database", type='primary', key="submit_btn")
        if submit_btn:
            # add additional data
            upload_datetime = datetime.now()
            upload_ip = perangkat_df[perangkat_df['nama_perangkat'] == perangkat]['ip'].values[0]
            preview_df = preview_df.assign(upload_datetime=upload_datetime,upload_ip=upload_ip)
            # append to database
            append_table(preview_df, f'{module}_table')
