import streamlit as st
import pandas as pd
from datetime import datetime
from sqlalchemy.sql import text


from extentions.converter import extract_module_32, extract_module_4

conn = st.connection('main_db', type='sql')
cursor = conn.connect()
st.write('hello world')

with open('statistics 32 module.txt','r') as f:
    module32 = f.readlines()

df = extract_module_32(module32)
df = pd.Dataframe(df)

upload_date = datetime.now()
upload_perangkat = 'Perangkat 1'
upload_ip = '38.0.101.76'

df = df.assign(tanggal_upload=upload_date,nama_perangkat=upload_perangkat,ip_address=upload_ip,tipe_perangkat='Perangkat 32 Modul')
df=df['upload_date','upload_perangkat','upload_ip','module','sim','net','grp','minutes','hhh:mmm','calls','reject','failed','c.offs','smses','%']

with conn.session as s:
    s.execute(text('DROP TABLE IF EXISTS module_32_table'))
    df.to_sql('module_32_table', cursor, if_exists='replace', index=False)
    s.commit()

with open('statistics(7).txt','r') as f:
    module4 = f.readlines()

df4 = extract_module_4(module4)
df4 = pd.Dataframe(df4)

upload_date = datetime.now()
upload_perangkat = 'Perangkat 1'
upload_ip = '38.0.101.76'

df4 = df4.assign(tanggal_upload=upload_date,nama_perangkat=upload_perangkat,ip_address=upload_ip,tipe_perangkat='Perangkat 4 Modul')
df4=df4['tanggal_upload','nama_perangkat', 'tipe_perangkat','ip_address','module','-','(reset)','minutes','hhh:mm:ss','calls','reject','failed','c.offs','smses','%']

with conn.session as s:
    s.execute(text('DROP TABLE IF EXISTS module_4_table'))
    df4.to_sql('module_4_table', cursor, if_exists='replace', index=False)
    s.commit()