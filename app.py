import streamlit as st


conn = st.connection('main_db', type='sql')
perangkat = conn.query('SELECT * FROM ip_address')

st.data_editor(perangkat, use_container_width=True, num_rows='dynamic')