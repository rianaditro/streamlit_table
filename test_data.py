import random
import pandas as pd
import streamlit as st

from extentions.new_entry import upload_data
from datetime import timedelta

conn = st.connection('main_db', type='sql', ttl=timedelta(minutes=59))

def get_df(module):
    calls = random.randint(0,100)
    failed = random.randint(0,100)
    asr = (calls/(calls+failed))*100

    if module == 'module_4':
        data = [{'module':0, '-':0, 'reset':0, 'minutes':0, 'hms':0, 'calls':calls, 'reject':0, 'failed':failed, 'coffs':0, 'smses':0,'asr':asr}]
    elif module == 'module_32':
        data = [{'module':0, 'sim':0, 'net':0, 'minutes':0, 'hms':0, 'calls':calls, 'reject':0, 'failed':failed, 'coffs':0, 'smses':0,'asr':asr}]
    elif module == 'module_ge':
        data = [{'mobile_port':0, 'port_status':0, 'signal_strength':0, 'call_duration':0, 'dialed_calls':0, 'successfull_calls':calls, 'asr':asr, 'acd':0, 'allocated_ammount':0, 'consumed_amount':0}]
    df = pd.DataFrame(data)
    return df


def test_job():
    ip = random.randint(111,999)
    module = ['module_4','module_32','module_ge']
    choosen_module = module[random.randint(0,2)]
    print(choosen_module)
    df = get_df(choosen_module)
    print(df)
    upload_data(conn, df, ip, choosen_module)
    print("uploaded")