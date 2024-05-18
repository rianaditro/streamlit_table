import streamlit as st
st.set_page_config(page_title="Home", page_icon="🏠", layout="wide", initial_sidebar_state='collapsed')

from extentions.report import report_section


conn = st.connection('main_db', type='sql')
# module 4
# col_order_4 = ['upload_datetime', 'upload_ip', 'module', '-', '(reset)', 'minutes', 'hhh:mmm', 'calls', 'reject', 'failed', 'c.offs', 'smses','%']
module_4_df = conn.query('SELECT * FROM module_4_table')
# module_4_df = module_4_df[col_order_4]
# module 32
# col_order_32 = ['upload_datetime', 'upload_ip', 'module', 'sim', 'net', 'grp', 'minutes', 'hhh:mmm', 'calls', 'reject', 'failed', 'c.offs', 'smses','%']
module_32_df = conn.query(f'SELECT * FROM module_32_table')
# module_32_df = module_32_df[col_order_32]

# frontend section
st.write("welcome")
st.subheader("Statistik Tabel Perangkat 4 Modul", anchor=False)
report_section(df=module_4_df, module='module_4')
st.divider()
st.subheader("Statistik Tabel Perangkat 32 Modul", anchor=False)
report_section(df=module_32_df, module='module_32')