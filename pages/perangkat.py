import streamlit as st
from sqlalchemy.sql import text


def clear_cache():
    st.cache_data.clear()
    st.cache_resource.clear()
    st.rerun()

def perangkat_main():    
    conn = st.connection('main_db', type='sql')
    perangkat_df = conn.query('SELECT * FROM perangkat_table')
    # frontend section
    st.subheader("Manajemen Perangkat", anchor=False)
    edited_perangkat_df = st.data_editor(perangkat_df, use_container_width=True,
                                        num_rows='dynamic',
                                        column_config={
                                            'tipe_perangkat':st.column_config.SelectboxColumn("Tipe Perangkat", 
                                                                            options=['Perangkat GE', 'Perangkat 4 Modul', 'Perangkat 32 Modul'])})

    save = st.button("Simpan Perubahan", key="change_ip_btn", type='primary')
    if save:
        with conn.session as s:
            s.execute(text('DELETE FROM perangkat_table'))
            for index, row in edited_perangkat_df.iterrows():
                s.execute(text(f"INSERT INTO perangkat_table (nama_perangkat, ip_address, tipe_perangkat) VALUES (\'{row['nama_perangkat']}\', \'{row['ip_address']}\', \'{row['tipe_perangkat']}\')"))
            s.commit()
        clear_cache()
