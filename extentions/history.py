import streamlit as st


conn = st.connection('main_db', type='sql')


def update_table(module_filter):
    if module_filter == 'All':
        history_data = conn.query(f'SELECT * FROM history_table ORDER BY upload_datetime DESC')
    else:
        history_data = conn.query(f'SELECT * FROM history_table WHERE module = "{module_filter}" ORDER BY upload_datetime DESC')
    return history_data

def history_section(module:str):
    st.subheader("Riwayat Upload", anchor=False)
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            st.write("Lihat riwayat:")
        with col2:
            if module == 'module_4':
                module_filter_index = 1
            elif module == 'module_32':
                module_filter_index = 2
            else:
                module_filter_index = 0
            module_filter = st.selectbox('', options=['All', 'Perangkat 4 Modul', 'Perangkat 32 Modul'], index=module_filter_index, label_visibility='hidden')
        
        history_data = update_table(module_filter)
        st.dataframe(history_data, use_container_width=True, hide_index=True)
        
