import streamlit as st


def update_table(conn, module_filter):
    if module_filter == 'All':
        history_data = conn.query(f'''
                                  SELECT h.upload_id, h.upload_datetime, h.ip_address, p.nama_perangkat, p.tipe_perangkat FROM history_upload as h 
                                  JOIN perangkat_table as p 
                                  ON h.ip_address = p.ip_address 
                                  ORDER BY h.upload_datetime DESC''')
    else:
        history_data = conn.query(f'''
                                  SELECT h.upload_id, h.upload_datetime, h.ip_address, p.nama_perangkat, p.tipe_perangkat FROM history_upload as h 
                                  JOIN perangkat_table as p 
                                  ON h.ip_address = p.ip_address
                                  WHERE tipe_perangkat = "{module_filter}"
                                  ORDER BY h.upload_datetime DESC''')
    return history_data

def history_section(conn, module:str):
    st.subheader("Riwayat Upload", anchor=False)
    with st.container(border=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            if module == 'module_4':
                module_filter_index = 1
            elif module == 'module_32':
                module_filter_index = 2
            elif module == 'module_ge':
                module_filter_index = 3
            else:
                module_filter_index = 0
            module_filter = st.selectbox('Lihat Riwayat:', 
                                         options=['All', 'Perangkat 4 Modul', 'Perangkat 32 Modul', 'Perangkat GE'], 
                                         index=module_filter_index)
        
        history_data = update_table(conn, module_filter)
        st.dataframe(history_data, use_container_width=True, hide_index=True)
        
