#!/usr/bin/env python3

from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from time import sleep
from random import randint
from dotenv import load_dotenv
load_dotenv()
import os
from xvfbwrapper import Xvfb

from ExternalIp import ExternalIp

vdisplay = Xvfb(width=1920, height=1080, colordepth=24)
vdisplay.start()

def random_delay(max_value=10):
    delay = randint(0, max_value) 
    print('random_delay max: {}, selected: {}'.format(max_value, delay))
    sleep(delay)

def css_selector_click(css_selector):
    input_element = driver.find_element_by_css_selector(css_selector)
    random_delay(2)
    input_element.click()

def enter_input(css_selector, value):
    input_element = driver.find_element_by_css_selector(css_selector)
    random_delay(2)
    input_element.click()
    random_delay(2)
    input_element.send_keys(value)

chrome_options = Options()
chrome_options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=chrome_options)

def get_external_ip():
    return str(ExternalIp())

def main():
    print('getting external ip')
    external_ip = get_external_ip()
    print('external_ip: ', external_ip)

    print('logging in namecheap')
    driver.get("https://www.namecheap.com/myaccount/login/")

    random_delay(10)

    enter_input("input[name=LoginUserName].nc_username",os.getenv('NAMECHEAP_USERNAME'))

    print('username entered')
    random_delay(10)

    enter_input("input[name=LoginPassword].nc_password",os.getenv('NAMECHEAP_PASSWORD'))

    print('password entered')
    random_delay(5)

    css_selector_click('input[type=submit].nc_login_submit')
    print('submit pressed')

    random_delay(5)

    print('change url to domain control panel')
    driver.get('https://ap.www.namecheap.com/Domains/DomainControlPanel/{}/advancedns'.format(os.getenv('NAMECHEAP_DOMAIN_NAME')))

    sleep(3)
    random_delay(2)

    host_records_table = driver.find_elements_by_css_selector('table')[0]
    print('host_records_table', host_records_table)

    print('scrolling to table with host records')
    driver.execute_script("arguments[0].scrollIntoView(true);", host_records_table);
    driver.execute_script("arguments[0].scrollIntoView(true);", host_records_table);

    ip_inputs = host_records_table.find_elements_by_css_selector('td.value')
    print('ip_inputs', ip_inputs)

    for p in ip_inputs:
        print('p.click()')
        try:
            p.click()
        except ElementClickInterceptedException as e:
            print('ElementClickInterceptedException')
            pass
        random_delay(2)

    print('clicked on the all ip inputs')

    inputs = driver.find_elements_by_css_selector('td.value input')
    for i in inputs:
        random_delay(2)
        driver.execute_script('arguments[0].value = "{}"'.format(external_ip), i)

    print('changed ip to {}'.format(external_ip))

    save_button = driver.find_element_by_css_selector('table.advanced-dns a.text-green')
    save_button.click()

    print('pressed save button')

    driver.close()
    vdisplay.stop()

if __name__ == "__main__":
    main()
