import streamlit as st
import schedule, datetime
import time
import logging

from sqlalchemy import text
from datetime import timedelta
from datetime import date
from scrap import Scraper
from extentions.new_entry import upload_data

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# get list of ip address
conn = st.connection('main_db', type='sql', ttl=timedelta(minutes=59))
ip_df = conn.query('SELECT ip_address, tipe_perangkat FROM perangkat_table')

def info(message):
    logging.info(message)
    print(message)

def get_ip_list(df, module):
    ip_list = df[df['tipe_perangkat'] == module]['ip_address'].tolist()
    return ip_list    

vbm_ip_list = get_ip_list(ip_df, 'Perangkat 4 Modul')
ge_ip_list = get_ip_list(ip_df, 'Perangkat GE')
se_ip_list = get_ip_list(ip_df, 'Perangkat 32 Modul')

def scrap_list(scraper, ip_list, module):
    info(f"Scraping {len(ip_list)} of IP Address from {module}")
    for ip in ip_list:
        try:
            df = scraper.get_data(ip, module)
            upload_data(conn, df, ip, module)
            info("Data uploaded to database")
        except Exception as e:
            info(f"Failed to upload data to database: {e}")
            logging.warning(f"Failed to scrape {ip}")

def scrap_job():
    scraper = Scraper()
    info("===================== Updating Data =====================")
    scrap_list(scraper, vbm_ip_list, 'module_4')
    scrap_list(scraper, se_ip_list, 'module_32')
    scrap_list(scraper, ge_ip_list, 'module_ge')
    info("===================== Data Updated =====================")
    del scraper

def daily_delete():
    limit_date = date.today() - timedelta(days=2)
    limit_id = limit_date.strftime("%Y%m%d")
    with conn.session as s:
        s.execute(text('DELETE FROM module_4_table WHERE upload_id LIKE "limit_id%"'))
        s.execute(text('DELETE FROM module_32_table WHERE upload_id LIKE "limit_id%"'))
        s.execute(text('DELETE FROM module_ge_table WHERE upload_id LIKE "limit_id%"'))
        s.execute(text('DELETE FROM history_upload WHERE upload_id LIKE "limit_id%"'))
        s.commit()

# Schedule the jobs
schedule.every(2).hours.at("59:59").do(scrap_job)
schedule.every().day.at("00:00").do(daily_delete)

# Function to run the scheduler
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    info("Auto-update data started")
    daily_delete()
    scrap_job()
    try:
        print("Program is running, please let this window open")
        run_scheduler()
    except Exception as e:
        print(e)
        info("Auto-update data stopped")