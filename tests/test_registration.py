# TC01 - Registration

# imports:

import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import csv
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1420,1080')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

driver = webdriver.ChromeChromeDriverManager().install()
wait = WebDriverWait(driver, 10)


def find_and_clear(xpath):
    element = driver.find_element_by_xpath(xpath)
    element.clear()
    return element


def test_registration():
    driver.get('http://localhost:1667/#/register')
    time.sleep(2)

    try:

        sign_up_button = driver.find_element_by_class_name('btn')

        with open('registration.csv', 'r') as reg:
            csv_reader = csv.reader(reg, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                find_and_clear('//*[@id="app"]/div/div/div/div/form/fieldset[1]/input').send_keys(row[0])
                find_and_clear('//*[@id="app"]/div/div/div/div/form/fieldset[2]/input').send_keys(row[1])
                find_and_clear('//*[@id="app"]/div/div/div/div/form/fieldset[3]/input').send_keys(row[2])
                sign_up_button.click()
    # Failed registration:
                registration_failed_message_is_visible = wait.until(
                    EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div[3]")))
                registration_failed_message = driver.find_element_by_xpath('/html/body/div[2]/div/div[3]').text
                ok_button = driver.find_element_by_xpath('/html/body/div[2]/div/div[4]/div/button')

                if registration_failed_message == 'Email must be a valid email.':
                    ok_button.click()
                elif registration_failed_message == 'Email already taken.':
                    ok_button.click()
                elif registration_failed_message == 'Username field required.':
                    ok_button.click()
                elif registration_failed_message == 'Email field required.':
                    ok_button.click()
                else:
                    ok_button.click()
    finally:
        driver.close()

