#!/usr/bin/env python3

from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from time import sleep
from random import randint
from dotenv import load_dotenv
load_dotenv()
import os

def random_delay(max_value=10):
    sleep(randint(0, max_value))

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

driver = webdriver.Chrome()

def get_external_ip():
    driver.get("https://ifconfig.me")
    ip = driver.find_element_by_id("ip_address")
    print(ip.text)
    return ip.text

def main():
    external_ip = get_external_ip()

    driver.get("https://www.namecheap.com/myaccount/login/")

    random_delay(10)

    enter_input("input[name=LoginUserName].nc_username",os.getenv('NAMECHEAP_USERNAME'))

    random_delay(10)

    enter_input("input[name=LoginPassword].nc_password",os.getenv('NAMECHEAP_PASSWORD'))

    random_delay(5)

    css_selector_click('input[type=submit].nc_login_submit')

    random_delay(5)

    driver.get('https://ap.www.namecheap.com/Domains/DomainControlPanel/{}/advancedns'.format(os.getenv('NAMECHEAP_DOMAIN_NAME')))

    sleep(3)
    random_delay(2)

    host_records_table = driver.find_elements_by_css_selector('table')[0]
    print('host_records_table', host_records_table)

    driver.execute_script("arguments[0].scrollIntoView(true);", host_records_table);
    driver.execute_script("arguments[0].scrollIntoView(true);", host_records_table);
    # import pdb; pdb.set_trace()

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

    inputs = driver.find_elements_by_css_selector('td.value input')
    for i in inputs:
        random_delay(2)
        driver.execute_script('arguments[0].value = "{}"'.format(external_ip), i)

    # import pdb; pdb.set_trace()
    save_button = driver.find_element_by_css_selector('table.advanced-dns a.text-green')
    save_button.click()

    driver.close()

if __name__ == "__main__":
    main()
