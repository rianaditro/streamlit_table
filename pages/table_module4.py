import streamlit as st

from io import StringIO

from converter import extract_module_4

conn = st.connection('main_db', type='sql')
perangkat_df = conn.query('SELECT * FROM ip_address')
daftar_perangkat = perangkat_df['nama_perangkat'].tolist()


perangkat = st.selectbox('Pilih Perangkat', options=daftar_perangkat, placeholder='Pilih Perangkat')
upload = st.file_uploader('Pilih File', type='txt', accept_multiple_files=False)

if upload:
    txt = StringIO(upload.getvalue().decode("utf-8")).readlines()
    module_4_df = extract_module_4(txt)
    st.dataframe(module_4_df, use_container_width=True)