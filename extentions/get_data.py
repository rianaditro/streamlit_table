import streamlit as st

from datetime import timedelta


@st.cache_data(ttl=timedelta(minutes=59))
def table_data(_conn, module):
    data = _conn.query(f'SELECT * FROM {module}_table')
    return data