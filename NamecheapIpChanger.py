#!/usr/bin/env python3

import os
import logging
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from time import sleep
from random import randint
from dotenv import load_dotenv
from xvfbwrapper import Xvfb

from ExternalIp import ExternalIp


class NamecheapIpChanger:

    def __init__(self, external_ip=None):
        logging.basicConfig(filename='namecheap_ip_changer.log', level=logging.DEBUG)
        if not os.getenv('DEBUG_IP_CHANGER'):
            self.vdisplay = Xvfb(width=1920, height=1080, colordepth=24, fbdir="/tmp/")
            self.vdisplay.start()

        chrome_options = Options()
        chrome_options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(options=chrome_options)

        if external_ip == None:
            external_ip = str(ExternalIp())
        self.external_ip = external_ip

    def cleanup(self):
        if not os.getenv('DEBUG_IP_CHANGER'):
            self.driver.close()
            self.vdisplay.stop()

    def change_ip(self):
        load_dotenv()

        self._login()

        host_records_table = self.__find_host_records_table()

        self.__enter_external_ip_to_records_table(host_records_table)


    def _login(self):
        logging.debug('logging in namecheap')
        self.driver.get("https://www.namecheap.com/myaccount/login/")

        self._random_delay(10)

        self._enter_input("input[name=LoginUserName].nc_username", os.getenv('NAMECHEAP_USERNAME'))

        logging.debug('username entered')
        self._random_delay(10)

        self._enter_input("input[name=LoginPassword].nc_password", os.getenv('NAMECHEAP_PASSWORD'))

        logging.debug('password entered')
        self._random_delay(5)

        self._css_selector_click('input[type=submit].nc_login_submit')
        logging.debug('submit pressed')

    def __find_host_records_table(self):
        self._random_delay(5)
        logging.debug('change url to domain control panel')
        self.driver.get('https://ap.www.namecheap.com/Domains/DomainControlPanel/{}/advancedns'
                        .format(os.getenv('NAMECHEAP_DOMAIN_NAME')))
        sleep(3)
        self._random_delay(2)

        host_records_table = self.driver.find_elements_by_css_selector('table')[0]
        logging.debug('host_records_table {}'.format(host_records_table))

        logging.debug('scrolling to table with host records')
        self.driver.execute_script("arguments[0].scrollIntoView(true);", host_records_table)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", host_records_table)
        return host_records_table

    def __enter_external_ip_to_records_table(self, host_records_table):
        ip_inputs = host_records_table.find_elements_by_css_selector('td.value')
        logging.debug('ip_inputs {}'.format(ip_inputs))

        for p in ip_inputs:
            logging.debug('p.click()')
            try:
                p.click()
            except ElementClickInterceptedException as e:
                logging.debug('ElementClickInterceptedException')
                pass
            self._random_delay(2)

        logging.debug('clicked on the all ip inputs')

        inputs = self.driver.find_elements_by_css_selector('td.value input')
        for i in inputs:
            self._random_delay(2)
            self.driver.execute_script('arguments[0].value = "{}"'.format(self.external_ip), i)

        logging.debug('changed ip to {}'.format(self.external_ip))

        save_button = self.driver.find_element_by_css_selector('table.advanced-dns a.text-green')
        save_button.click()

        logging.debug('pressed save button')


    def _random_delay(self, max_value=10):
        delay = randint(0, max_value)
        logging.debug('self._random_delay max: {}, selected: {}'.format(max_value, delay))
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
