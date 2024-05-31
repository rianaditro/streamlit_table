from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs4
from io import StringIO

from extentions.converter import extract_module_32, extract_module_4

import pandas as pd, logging


def info(message):
    logging.info(message)
    print(message)

class Scraper:
    def __init__(self):
        self.driver = self.get_driver()
        self.ip_address = None
        self.html = None
        self.html2 = None
        self.html3 = None

    def get_driver(self):
        options = Options()
        options.add_argument("start-maximized")
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--enable-javascript')
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        return driver
    
    def login(self, module:str):
        if module != 'module_ge':
            username_field = self.driver.find_element(By.NAME, 'user')
            password_field = self.driver.find_element(By.NAME, 'pass')
            username_field.send_keys('Admin')
            password_field.send_keys('2n')
        else: 
            frame = self.driver.find_element(By.ID, "UserWin")
            self.driver.switch_to.frame(frame)
            password_field = self.driver.find_element(By.NAME, 'LOGIN_PASSWORD')
            password_field.send_keys('Artatel@8900')
        password_field.send_keys(Keys.RETURN)
        info(f"Logged into {self.ip_address}")

    def get_html(self, ip_address, module:str):
        try:
            url = f'https://{ip_address}'
            self.driver.get(url)
        except:
            url = f'http://{ip_address}'
            self.driver.get(url)
        self.login(module=module)
        # if not GE then VBM or SG
        if module != 'module_ge':
            self.driver.get(f'{url}/?section=3')
            self.html = self.driver.page_source
        else:
            # Page is divided by 3 sub page
            self.driver.get(f'{url}/MobileStatus.html?SubPageIndex=1')
            self.html = self.driver.page_source
            self.driver.get(f'{url}/MobileStatus.html?SubPageIndex=2')
            self.html2 = self.driver.page_source
            self.driver.get(f'{url}/MobileStatus.html?SubPageIndex=3')
            self.html3 = self.driver.page_source

    def get_data(self, ip_address, module:str='GE'):
        self.ip_address = ip_address
        self.get_html(ip_address, module=module)
        if module != 'module_ge':
            soup = bs4(self.html, 'html.parser')
            hidden_data = soup.find_all('input', type='hidden', attrs={'name':'save_data'})
            result = [data.get('value') for data in hidden_data]
            if module == 'module_4':
                extracted_data = extract_module_4(result)
            elif module == 'module_32':
                extracted_data = extract_module_32(result)
            df = pd.DataFrame(extracted_data)
            info(f"Data extracted from {self.ip_address}")
            return df
        else:
            def extract_table(html):
                df = pd.read_html(StringIO(html))[-2]
                df = df[[1,6,9,10,11,12,13,20,21]]
                df.rename(columns={1:'port_status', 6:'signal_strength', 
                                   9:'call_duration', 10:'dialed_calls', 11:'successfull_calls', 
                                   12:'asr', 13:'acd', 20:'allocated_ammount', 21:'consumed_amount'}, inplace=True)
                return df

            df = extract_table(self.html)
            df2 = extract_table(self.html2)
            df3 = extract_table(self.html3)
            df = pd.concat([df, df2, df3])
            df.reset_index()
            df['mobile_port'] = range(1, len(df) + 1)
            column_order = ['mobile_port']+[col for col in df.columns if col != 'mobile_port']
            df = df[column_order]
            info(f"Data extracted from {self.ip_address}")
            return df

if __name__ == "__main__":
    from extentions.new_entry import upload_data
    import streamlit as st
    conn = st.connection('main_db', type='sql')
    url = "https://192.168.110.169"
    scraper = Scraper()
    df = scraper.get_data(url, module='module_ge')
    upload_data(df, url, 'module_ge')

    