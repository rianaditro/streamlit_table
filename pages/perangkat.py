import streamlit as st
from sqlalchemy.sql import text


conn = st.connection('main_db', type='sql')
perangkat_df = conn.query('SELECT * FROM ip_address')

st.subheader("Manajemen Perangkat", anchor=False)
edited_perangkat_df = st.data_editor(perangkat_df, use_container_width=True, num_rows='dynamic')

save = st.button("Simpan Perubahan", key="change_ip_btn", type='primary')
if save:
    with conn.session as s:
        s.execute(text('DELETE FROM ip_address'))
        for index, row in edited_perangkat_df.iterrows():
            s.execute(text(f"INSERT INTO ip_address (nama_perangkat, ip) VALUES (\'{row['nama_perangkat']}\', \'{row['ip']}\')"))
        s.commit()
    st.rerun()