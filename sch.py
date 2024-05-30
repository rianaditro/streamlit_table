import streamlit as st
import schedule
import time
import logging

from add_data import new_data
from extentions.new_entry import upload_data

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# get list of ip address
conn = st.connection('main_db', type='sql')
ip_df = conn.query('SELECT ip_address, tipe_perangkat FROM perangkat_table')

def get_ip_list(df, module):
    return df[df['tipe_perangkat'] == module]['ip_address'].tolist()

vbm_ip_list = get_ip_list(ip_df, 'Perangkat 4 Modul')
ge_ip_list = get_ip_list(ip_df, 'Perangkat GE')
se_ip_list = get_ip_list(ip_df, 'Perangkat 32 Modul')

def scrap_list(ip_list, module):
    logging.info(f"Scraping {len(ip_list)} of IP Address from {module}")
    for ip in ip_list:
        df = new_data(module)
        upload_data(df, ip, module)

def scrap_job():
    logging.info("===================== Scraping task started =====================")
    scrap_list(vbm_ip_list, 'module_4')
    scrap_list(se_ip_list, 'module_32')
    scrap_list(ge_ip_list, 'module_ge')
    logging.info("===================== Scraping task ended =====================")

def job():
    scrap_job()

# Schedule the jobs
schedule.every().minute.do(job)

# Function to run the scheduler
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    logging.info("Auto-update data started")
    try:
        print("Program is running, please let this window open")
        run_scheduler()
    except KeyboardInterrupt:
        logging.info("Scheduler stopped")
        print("Auto-update data stopped")