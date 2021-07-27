# TC02 - Login

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import csv
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from os import getcwd



def test_login():

    options = Options()
    options.headless = True

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    wait = WebDriverWait(driver, 10)
    cwd = getcwd()

    try:
        driver.get('http://localhost:1667/#/login')

        def find_and_clear(element_xpath):
            element = driver.find_element_by_xpath(element_xpath)
            element.clear()
            return element

        sign_in_button = driver.find_element_by_xpath('//*[@id="app"]/div/div/div/div/form/button')

        # data entry:
        with open(cwd + 'login.csv', 'r') as login_data:
            login_data_reader = csv.reader(login_data, delimiter=',')
            next(login_data_reader)
            for row in login_data_reader:
                find_and_clear('//*[@id="app"]/div/div/div/div/form/fieldset[1]/input').send_keys(row[0])  # email
                find_and_clear('//*[@id="app"]/div/div/div/div/form/fieldset[2]/input').send_keys(row[1])  # password

                sign_in_button.click()
                try:
                    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/nav/div/ul/li[4]/a')))

                    user = driver.find_element_by_xpath('//*[@id="app"]/nav/div/ul/li[4]/a').text
                    assert user == row[2]

                    # log out
                    logout = driver.find_element_by_xpath('//*[@id="app"]/nav/div/ul/li[5]/a')
                    logout.click()

                    # navigate to sign in
                    sign_in_link = driver.find_element_by_xpath('//*[@id="app"]/nav/div/ul/li[2]/a')
                    sign_in_link.click()
                except:
                    # failed message:
                    login_failed_is_visible = wait.until(
                        EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div/div[2]')))
                    login_failed_message = driver.find_element_by_xpath('/html/body/div[2]/div/div[3]').text
                    login_failed_ok_button = driver.find_element_by_xpath('/html/body/div[2]/div/div[4]/div/button')

                    if login_failed_message == 'Email field required.':
                        login_failed_ok_button.click()
                    elif login_failed_message == 'Invalid user credentials.':
                        login_failed_ok_button.click()

    finally:
        driver.close()
