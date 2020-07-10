#!/usr/bin/env python3

from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from time import sleep
from random import randint
from dotenv import load_dotenv
import os
from xvfbwrapper import Xvfb

from ExternalIp import ExternalIp



class NamecheapIpChanger:

    def __init__(self, external_ip=None):
        self.vdisplay = Xvfb(width=1920, height=1080, colordepth=24, fbdir="/tmp/")
        self.vdisplay.start()

        chrome_options = Options()
        chrome_options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(options=chrome_options)

        if external_ip == None:
            external_ip = str(ExternalIp())
        self.external_ip = external_ip

    def cleanup(self):
        self.driver.close()
        self.vdisplay.stop()

    def change_ip(self):
        load_dotenv()

        self._login()

        host_records_table = self.__find_host_records_table()

        self.__enter_external_ip_to_records_table(host_records_table)


    def _login(self):
        print('logging in namecheap')
        self.driver.get("https://www.namecheap.com/myaccount/login/")

        self._random_delay(10)

        self._enter_input("input[name=LoginUserName].nc_username",os.getenv('NAMECHEAP_USERNAME'))

        print('username entered')
        self._random_delay(10)

        self._enter_input("input[name=LoginPassword].nc_password",os.getenv('NAMECHEAP_PASSWORD'))

        print('password entered')
        self._random_delay(5)

        self._css_selector_click('input[type=submit].nc_login_submit')
        print('submit pressed')

    def __find_host_records_table(self):
        self._random_delay(5)
        print('change url to domain control panel')
        self.driver.get('https://ap.www.namecheap.com/Domains/DomainControlPanel/{}/advancedns'.format(os.getenv('NAMECHEAP_DOMAIN_NAME')))
        sleep(3)
        self._random_delay(2)

        host_records_table = self.driver.find_elements_by_css_selector('table')[0]
        print('host_records_table', host_records_table)

        print('scrolling to table with host records')
        self.driver.execute_script("arguments[0].scrollIntoView(true);", host_records_table);
        self.driver.execute_script("arguments[0].scrollIntoView(true);", host_records_table);
        return host_records_table

    def __enter_external_ip_to_records_table(self, host_records_table):
        ip_inputs = host_records_table.find_elements_by_css_selector('td.value')
        print('ip_inputs', ip_inputs)

        for p in ip_inputs:
            print('p.click()')
            try:
                p.click()
            except ElementClickInterceptedException as e:
                print('ElementClickInterceptedException')
                pass
            self._random_delay(2)

        print('clicked on the all ip inputs')

        inputs = self.driver.find_elements_by_css_selector('td.value input')
        for i in inputs:
            self._random_delay(2)
            self.driver.execute_script('arguments[0].value = "{}"'.format(self.external_ip), i)

        print('changed ip to {}'.format(self.external_ip))

        save_button = self.driver.find_element_by_css_selector('table.advanced-dns a.text-green')
        save_button.click()

        print('pressed save button')


    def _random_delay(self, max_value=10):
        delay = randint(0, max_value) 
        print('self._random_delay max: {}, selected: {}'.format(max_value, delay))
        sleep(delay)

    def _css_selector_click(self, css_selector):
        input_element = self.driver.find_element_by_css_selector(css_selector)
        self._random_delay(2)
        input_element.click()

    def _enter_input(self, css_selector, value):
        input_element = self.driver.find_element_by_css_selector(css_selector)
        self._random_delay(2)
        input_element.click()
        self._random_delay(2)
        input_element.send_keys(value)


def main():
    ip_changer = NamecheapIpChanger()
    ip_changer.change_ip()
    ip_changer.cleanup()

if __name__ == "__main__":
    main()
