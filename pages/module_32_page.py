import streamlit as st

from extentions.report import report_section
from extentions.new_entry import entry_section


def module_32_main():
    conn = st.connection('main_db', type='sql')
    module = 'module_32'
    module_df = conn.query(f'SELECT * FROM {module}_table')


    # frontend section
    st.subheader("Statistik Tabel Perangkat 32 Modul", anchor=False)
    report_section(df=module_df, module=module)
    st.divider()
    entry_section(conn=conn, module=module)
