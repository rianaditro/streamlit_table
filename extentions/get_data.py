import streamlit as st

from datetime import timedelta


@st.cache_data(ttl=timedelta(minutes=10))
def table_data(_conn, module):
    data = _conn.query(f'SELECT * FROM {module}_table ORDER BY upload_datetime DESC')
    return data