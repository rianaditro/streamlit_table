import streamlit as st

from extentions.report import report_section
from extentions.history import history_section


def ge_main_module(conn):
    module = 'module_ge'
    module_df = conn.query(f'SELECT * FROM {module}_table')

    # frontend section
    st.subheader("Statistik Tabel Perangkat GE", anchor=False)
    report_section(conn, df=module_df, module=module)
    st.divider()
    history_section(conn, module=module)
    st.divider()
    # entry_section(conn=conn, module=module)



