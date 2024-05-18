import streamlit as st
import pandas as pd

from io import StringIO
from datetime import datetime

from converter import extract_module_4

conn = st.connection('main_db', type='sql')
perangkat_df = conn.query('SELECT * FROM ip_address')
daftar_perangkat = perangkat_df['nama_perangkat'].tolist()


perangkat = st.selectbox('Pilih Perangkat', options=daftar_perangkat, placeholder='Pilih Perangkat')
upload = st.file_uploader('Pilih File', type='txt', accept_multiple_files=False)

if upload:
    txt = StringIO(upload.getvalue().decode("utf-8")).readlines()
    module_4_df = extract_module_4(txt)
    module_4_df = pd.DataFrame(module_4_df)
    upload_datetime = datetime.now()
    upload_perangkat = perangkat
    upload_ip = perangkat_df[perangkat_df['nama_perangkat'] == perangkat]['ip'].values[0]
    module_4_df = module_4_df.assign(upload_datetime=upload_datetime, upload_perangkat=upload_perangkat, upload_ip=upload_ip)
    st.dataframe(module_4_df, use_container_width=True, hide_index=True)