import streamlit as st

from extentions.report import report_section
from extentions.new_entry import entry_section

conn = st.connection('main_db', type='sql')
module = 'module_4'
col_order = ['upload_datetime', 'upload_ip', 'module', '-', '(reset)', 'minutes', 'hhh:mmm', 'calls', 'reject', 'failed', 'c.offs', 'smses','%']
module_df = conn.query(f'SELECT * FROM {module}_table')
module_df = module_df[col_order]


# frontend section
st.subheader("Statistik Tabel Perangkat 4 Modul", anchor=False)
report_section(df=module_df, module=module)
st.divider()
entry_section(conn=conn, module=module)
