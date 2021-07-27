# TC04 - Cookie Policy - accept

import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--disable-extensions')


def test_cookie_policy_accept():
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    try:
        driver.get('http://localhost:1667')

        # learn more:
        learn_more = driver.find_element_by_xpath('//div[@id="cookie-policy-panel"]//a')
        learn_more.click()
        cookie_policy = driver.switch_to.window(driver.window_handles[-1])
        time.sleep(3)
        driver.close()
        driver.switch_to.window((driver.window_handles[0]))

        # Accept:
        accept_button = driver.find_element_by_xpath('//div//button[contains(@class, "accept")]')
        accept_button.click()
    finally:
        driver.close()
