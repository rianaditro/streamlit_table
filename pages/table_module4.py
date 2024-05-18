import streamlit as st
import pandas as pd

from io import StringIO
from datetime import datetime
from sqlalchemy.sql import text

from converter import extract_module_4


conn = st.connection('main_db', type='sql')
cursor = conn.connect()

# get current data
view_data = conn.query('SELECT * FROM module_4_table')
col_order = ['upload_datetime', 'upload_perangkat', 'upload_ip', 'module', '-', '(reset)', 'minutes', 'hhh:mmm', 'calls', 'reject', 'failed', 'c.offs', 'smses','%']
col_config = {'upload_datetime':'Tanggal dan Waktu Upload', 'upload_perangkat':'Nama Perangkat', 'upload_ip':'IP Perangkat', 'module':'Modul', '-':'-', '(reset)':'(reset)', 'minutes':'Minutes', 'hhh:mmm':'HH:MM:SS', 'calls':'Calls', 'reject':'Reject', 'failed':'Failed', 'c.offs':'C.Offs', 'smses':'SMSes', '%':'%' }

# get data for selectbox
perangkat_df = conn.query('SELECT * FROM ip_address')
daftar_perangkat = perangkat_df['nama_perangkat'].tolist()

# msg
st.session_state.msg = None
if "file_uploader_key" not in st.session_state:
    st.session_state["file_uploader_key"] = 0


def clear_cache():
    st.cache_data.clear()
    st.cache_resource.clear()


st.subheader("Statistik Perangkat 4 Modul", anchor=False)
st.write("Tabel Terbaru")
st.dataframe(view_data, use_container_width=True, hide_index=True, column_order=col_order, column_config=col_config)
col1, col2 = st.columns(2)
with col1:
    export_btn = st.button("Export Tabel", type='primary', key="export_btn")
with col2:
    clear_btn = st.button("Hapus Tabel", type='secondary', key="clear_btn")
    if clear_btn:
        with conn.session as s:
            s.execute(text('DELETE FROM module_4_table'))
            s.commit()
        clear_cache()
        st.rerun()

st.divider()

# add new data
st.subheader("Tambah File", anchor=False)

perangkat = st.selectbox('Pilih Perangkat', options=daftar_perangkat, placeholder='Pilih Perangkat')
upload = st.file_uploader('Pilih File', type='txt', accept_multiple_files=False, key=st.session_state["file_uploader_key"])

if upload:
    txt = StringIO(upload.getvalue().decode("utf-8")).readlines()
    module_4_df = extract_module_4(txt)
    module_4_df = pd.DataFrame(module_4_df)
    st.write("Preview")
    st.dataframe(module_4_df, use_container_width=True, hide_index=True, column_order=col_order)

    submit_btn = st.button("Tambah ke Database", type='primary', key="submit_btn")
    if submit_btn:
        # add additional info
        upload_datetime = datetime.now()
        upload_perangkat = perangkat
        upload_ip = perangkat_df[perangkat_df['nama_perangkat'] == perangkat]['ip'].values[0]
        module_4_df = module_4_df.assign(upload_datetime=upload_datetime, upload_perangkat=upload_perangkat, upload_ip=upload_ip)

        # append into database
        module_4_df.to_sql('module_4_table', cursor, if_exists='append', index=False)
        clear_cache()
        st.session_state["file_uploader_key"] += 1
        del st.session_state[0]

        st.rerun()


