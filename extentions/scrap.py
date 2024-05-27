from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs4

from converter import extract_module_32, extract_module_4

import pandas as pd
import time


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
        # options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        return driver
    
    # default = True for VBM and SG Module
    def login(self, module:str='GE'):
        if module != 'GE':
            username_field = self.driver.find_element(By.NAME, 'user')
            password_field = self.driver.find_element(By.NAME, 'pass')
            username_field.send_keys('Admin')
            password_field.send_keys('2n')
        else: 
            time.sleep(3)
            password_field = self.driver.find_element(By.NAME, 'LOGIN_PASSWORD')
            password_field.send_keys('Artatel@8900')
        password_field.send_keys(Keys.RETURN)

    def get_html(self, ip_address, module:str='GE'):
    # check protocol connection
        def check_ip(ip_address, module):
            if module == 'GE':
                self.ip_address = f'https://{ip_address}'
            else:
                self.ip_address = f'http://{ip_address}'
        check_ip(ip_address, module)
        self.driver.get(self.ip_address)
        self.login(module=module)
        # if not GE then VBM or SG
        if module != 'GE':
            self.driver.get(f'{self.ip_address}/?section=3')
            self.html = self.driver.page_source
        else:
            # Page is divided by 3 sub page
            self.driver.get(f'{self.ip_address}/MobileStatus.html?SubPageIndex=1')
            self.html = self.driver.page_source
            self.driver.get(f'{self.ip_address}/MobileStatus.html?SubPageIndex=2')
            self.html2 = self.driver.page_source
            self.driver.get(f'{self.ip_address}/MobileStatus.html?SubPageIndex=3')
            self.html3 = self.driver.page_source
        

    def get_data(self, ip_address, module:str='GE'):
        self.get_html(ip_address, module=module)
        if module != 'GE':
            soup = bs4(self.html, 'html.parser')
            hidden_data = soup.find_all('input', type='hidden', attrs={'name':'save_data'})
            result = [data.get('value') for data in hidden_data]
            if module == 'VBM':
                extracted_data = extract_module_4(result)
            elif module == 'SG':
                extracted_data = extract_module_32(result)

            df = pd.DataFrame(extracted_data)
            return df
        else:
            def extract_table(html):
                df = pd.read_html(html)[-2]
                df = df[[1,6,9,10,11,12,13,20,21]]
                df.rename(columns={1:'Port Status', 6:'Signal Strenght', 
                                   9:'Call Duration', 10:'Dialed Calls', 11:'Successfull Calls', 
                                   12:'ASR', 13:'ACD', 20:'Allcated ammount', 21:'Used ammount'}, inplace=True)
                return df

            df = extract_table(self.html)
            df2 = extract_table(self.html2)
            df3 = extract_table(self.html3)
            df = pd.concat([df, df2, df3])
            df.reset_index()
            df['Mobile Port'] = df.index+1
            column_order = ['Mobile Port']+[col for col in df.columns if col != 'Mobile Port']
            df = df[column_order]
            return df


if __name__ == "__main__":

    '''
    GE still invalid
    VBM converter need additional adjustment
    '''
    # ge = '192.168.110.169'
    # vbm = '192.168.111.48'
    # se = '192.168.110.210'

    # scraper = Scraper()

    # ge_df = scraper.get_data(ge, module='GE')
    # vbm_df = scraper.get_data(vbm, module='VBM')
    # se_df = scraper.get_data(se, module='SG')

    # ge_df.to_excel('ge.xlsx', index=False)
    # vbm_df.to_excel('vbm.xlsx', index=False)
    # se_df.to_excel('se.xlsx', index=False)
    

