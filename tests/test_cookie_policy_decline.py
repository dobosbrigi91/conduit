# TC03 - Cookie Policy - decline

import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True

def test_cookie_policy_decline():
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    try:
        driver.get('http://localhost:1667')

        # learn more:
        learn_more = driver.find_element_by_xpath('//div[@id="cookie-policy-panel"]//a')
        learn_more.click()
        cookie_policy = driver.switch_to.window(driver.window_handles[-1])
        time.sleep(3)
        driver.close()
        driver.switch_to.window((driver.window_handles[0]))

        # decline:
        decline_button = driver.find_element_by_xpath('//div//button[contains(@class, "decline")]')
        decline_button.click()

    finally:
        driver.close()
