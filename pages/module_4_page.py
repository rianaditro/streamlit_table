import streamlit as st

from extentions.report import report_section
from extentions.new_entry import entry_section
from extentions.history import history_section


def module_4_main(conn):
    module = 'module_4'
    module_df = conn.query(f'SELECT * FROM {module}_table')

    # frontend section
    st.subheader("Statistik Tabel Perangkat 4 Modul", anchor=False)
    report_section(conn, df=module_df, module=module)
    st.divider()
    history_section(conn, module=module)
    st.divider()
    entry_section(conn, module=module)
