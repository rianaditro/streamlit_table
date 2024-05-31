import streamlit as st

from extentions.report import report_section
from extentions.new_entry import entry_section
from extentions.history import history_section
from extentions.get_data import table_data


def module_32_main(conn):
    module = 'module_32'
    module_df = table_data(conn, module)

    # frontend section
    st.subheader("Statistik Tabel Perangkat 32 Modul", anchor=False)
    report_section(conn, df=module_df, module=module)
    st.divider()
    history_section(conn, module=module)
    st.divider()
    entry_section(conn, module=module)
