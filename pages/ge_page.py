import streamlit as st

from extentions.report import report_section
from extentions.history import history_section
from extentions.get_data import table_data


def ge_main_module(conn):
    module = 'module_ge'
    module_df = table_data(conn, module)

    # frontend section
    st.subheader("Statistik Tabel Perangkat GE", anchor=False)
    report_section(conn, df=module_df, module=module)
    st.divider()
    history_section(conn, module=module)
    st.divider()
    # entry_section(conn=conn, module=module)



