# TC05 - New article

from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

def test_new_article():
    try:
        driver.get('http://localhost:1667/#/login')
        wait = WebDriverWait(driver, 10)

        # test user: email: testuser3@example.com password: Abcd123$
        driver.find_element_by_xpath('//fieldset//input[@placeholder="Email"]').send_keys('testuser3@example.com')
        driver.find_element_by_xpath('//fieldset//input[@placeholder="Password"]').send_keys('Abcd123$')
        driver.find_element_by_xpath('//form/button').click()
        time.sleep(2)
        test_user = driver.find_element_by_xpath('//nav/div/ul/li[4]/a')
        assert test_user.text == 'testuser3'

        # Navigate to New article
        new_article = driver.find_element_by_xpath('//nav/div/ul/li[2]/a')
        new_article.click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//form/fieldset/fieldset[1]/input')))

        # fields
        article_title = driver.find_element_by_xpath('//form/fieldset/fieldset[1]/input')
        whats_this_article_about = driver.find_element_by_xpath('//fieldset[2]/input')
        write_your_article = driver.find_element_by_xpath('//fieldset[3]/textarea')
        enter_tags = \
            driver.find_element_by_xpath('//*[@id="app"]/div/div/div/div/form/fieldset/fieldset[4]/div/div/ul/li/input')
        publish_article = driver.find_element_by_xpath('//button')

        # fields entry
        article_title.send_keys('Lorem Ipsum')
        whats_this_article_about.send_keys('What is Lorem Ipsum?')
        with open('newarticle.txt', 'r') as file:
            write_article = file.read()
            write_your_article.send_keys(write_article)
        enter_tags.send_keys('loremipsum')
        enter_tags.send_keys(Keys.ENTER)
        enter_tags.send_keys('lorem')
        publish_article.click()

        # check
        wait.until(EC.visibility_of_element_located((By.XPATH, '//div/div[1]/div/h1')))
        new_blog_title = driver.find_element_by_xpath('//div/div[1]/div/h1').text
        assert new_blog_title == 'Lorem Ipsum'
        time.sleep(2)

    finally:
        driver.close()
