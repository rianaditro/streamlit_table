import streamlit as st

from datetime import timedelta
from extentions.report import report_section
from extentions.new_entry import entry_section
from extentions.history import history_section


def ge_main_module():
    conn = st.connection('main_db', type='sql', ttl=timedelta(minutes=59))
    module = 'module_ge'
    module_df = conn.query(f'SELECT * FROM {module}_table')


    # frontend section
    st.subheader("Statistik Tabel Perangkat GE", anchor=False)
    report_section(df=module_df, module=module)
    st.divider()
    history_section(module=module)
    st.divider()
    # entry_section(conn=conn, module=module)



