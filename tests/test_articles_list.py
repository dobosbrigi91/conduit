# TC06 - Articles list

from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--disable-extensions')


def test_articles_list():
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    try:
        driver.get('http://localhost:1667/#/login')
        wait = WebDriverWait(driver, 10)

        # test user: email: testuser4@example.com password: Abcd123$

        driver.find_element_by_xpath('//fieldset//input[@placeholder="Email"]').send_keys('testuser4@example.com')
        driver.find_element_by_xpath('//fieldset//input[@placeholder="Password"]').send_keys('Abcd123$')
        driver.find_element_by_xpath('//form/button').click()
        time.sleep(2)
        test_user = driver.find_element_by_xpath('//nav/div/ul/li[4]/a')
        assert test_user.text == 'testuser4'

        # articles list:

        user_page = driver.find_element_by_xpath('//div[@class="container"]//ul/li[4]/a')
        user_page.click()

        # navigate to my articles:
        my_articles = driver.find_element_by_xpath('//ul[@class="nav nav-pills outline-active"]/li[1]')
        in_my_articles = driver.find_element_by_xpath('//ul[@class="nav nav-pills outline-active"]/li[1]/a')
        if in_my_articles.get_attribute('class') != 'nav-link router-link-exact-active active':
            in_my_articles.click()

        # title of articles save list and file
        time.sleep(3)
        wait_profile_page = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class="profile-page"]//h4')))
        articles = driver.find_elements_by_xpath('//div[@class="profile-page"]//h1')

        list_of_articles = []
        for row in articles:
            list_of_articles.append(row.text + '\n')
        print(list_of_articles)
        with open('user_articles.txt', 'w') as x:
            for item in list_of_articles:
                x.write(item)
    finally:
        driver.close()
