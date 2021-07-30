# TC02 - Login

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import csv
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException


def test_login():

    options = Options()
    options.headless = True

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

# # # # # # - def - # # # # # #

    def find_and_clear(element_xpath):
        element = driver.find_element_by_xpath(element_xpath)
        element.clear()
        return element

    def wait_to(element_xpath):
        wait = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, element_xpath)))
        if not wait:
            return False
        return True

    def element_click(element_xpath):
        button = driver.find_element_by_xpath(element_xpath)
        button.click()
        return button

# # # # # # - tests - # # # # # #

    try:
        driver.get('http://localhost:1667/#/login')
    # # log in and log out
        wait_to('//input[@placeholder="Email"]')  # visible email field

    # data entry:
        with open('tests/login.csv', 'r') as login_data:
            login_data_reader = csv.reader(login_data, delimiter=',')
            next(login_data_reader)
            for row in login_data_reader:
                find_and_clear('//*[@id="app"]/div/div/div/div/form/fieldset[1]/input').send_keys(row[0])  # email
                find_and_clear('//*[@id="app"]/div/div/div/div/form/fieldset[2]/input').send_keys(row[1])  # password
                element_click('//*[@id="app"]/div/div/div/div/form/button')  # sign in button
                try:
                    wait_to('//*[@id="app"]/nav/div/ul/li[4]/a')  # visible user name

                    username = driver.find_element_by_xpath('//*[@id="app"]/nav/div/ul/li[4]/a').text
                    assert username == row[2]
                    element_click('//*[@id="app"]/nav/div/ul/li[5]/a')
                    wait_to('//*[@id="app"]/nav/div/ul/li[2]/a')  # visible sing in
                    element_click('//*[@id="app"]/nav/div/ul/li[2]/a')
                except TimeoutException:
                    wait_to('/html/body/div[2]/div/div[2]')  # visible failed message
                    login_failed_message = driver.find_element_by_xpath('/html/body/div[2]/div/div[3]').text
                    if login_failed_message == 'Email field required.':
                        element_click('/html/body/div[2]/div/div[4]/div/button')
                    elif login_failed_message == 'Invalid user credentials.':
                        element_click('/html/body/div[2]/div/div[4]/div/button')  # failed message ok button
    finally:
        driver.close()
