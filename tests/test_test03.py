# new article, scrolling, list and save articles title, delete article, change username

# # # # # # - imports - # # # # # #
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options


def test_test03():
    # -  - #
    options = Options()
    options.headless = True

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get('http://localhost:1667/#/login')

    # # # # # # - def - # # # # # #

    def find(element_xpath):
        element = driver.find_element_by_xpath(element_xpath)
        return element

    def find_and_clear(element_xpath):
        element = driver.find_element_by_xpath(element_xpath)
        element.clear()
        return element

    def wait_to(element_xpath):
        wait = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, element_xpath)))
        if not wait:
            return False
        return True

    def element_click(element_xpath):
        button = driver.find_element_by_xpath(element_xpath)
        button.click()
        return button

    try:
        # # # # # # - tests - # # # # # #
        # # accept cookie policy

        element_click('//div[@id="cookie-policy-panel"]//a')  # learn more

        cookie_policy = driver.switch_to.window(driver.window_handles[-1])
        time.sleep(5)
        driver.close()
        driver.switch_to.window((driver.window_handles[0]))

        # Accept:
        element_click('//div//button[contains(@class, "accept")]')  # accept cookie policy

        # # new article
        # test user: email: testuser3@example.com password: Abcd123$ log in

        find_and_clear('//*[@id="app"]/div/div/div/div/form/fieldset[1]/input').send_keys('testuser3@example.com')
        # email
        find_and_clear('//*[@id="app"]/div/div/div/div/form/fieldset[2]/input').send_keys('Abcd123$')
        # password
        element_click('//*[@id="app"]/div/div/div/div/form/button')  # sign in button
        wait_to('//*[@id="app"]/nav/div/ul/li[4]/a')  # visible user name
        username = driver.find_element_by_xpath('//*[@id="app"]/nav/div/ul/li[4]/a').text
        assert username == 'testuser3'

        # Navigate to New article
        element_click('//nav/div/ul/li[2]/a')  # new article
        wait_to('//form/fieldset/fieldset[1]/input')  # visible article title field

        # fields
        find('//form/fieldset/fieldset[1]/input').send_keys('Hello')  # Title
        find('//fieldset[2]/input').send_keys('World')  # Whats this article about
        find('//fieldset[3]/textarea').send_keys('Hello World! Have a nice day')  # Write your article
        find('//*[@id="app"]/div/div/div/div/form/fieldset/fieldset[4]/div/div/ul/li/input').send_keys('hello')
        # enter tags
        wait_to('//button')
        element_click('//button')

        # article details
        wait_to('//*[@id="app"]/div/div[1]/div/h1')  # Title visible
        assert find('//*[@id="app"]/div/div[1]/div/h1').text == 'Hello'  # Title
        assert find('//*[@id="app"]/div/div[2]/div[1]/div/div[1]/p').text == 'Hello World! Have a nice day'  # article

        # # scroll through the page numbers

        # navigate home page
        wait_to('//li[@class="nav-item"][1]/a')
        element_click('//li[@class="nav-item"][1]/a')

        page_numbers = driver.find_elements_by_xpath('//*[@id="app"]/div/div[2]/div/div[1]/div[2]/div/div/nav/ul/li')
        for page in page_numbers:
            x_path = '//*[@id="app"]/div/div[2]/div/div[1]/div[2]/div/div/nav/ul/li[' + page.text + ']/a'
            find(x_path).click()
            wait_to('//*[@id="app"]/div/div[2]/div/div[1]/div[1]/ul/li[2]/a')  # visible Global feed

            # # user articles list:
        element_click('//div[@class="container"]//ul/li[4]/a')  # user page

        # title of articles save list and file
        wait_to('//div[@class="profile-page"]//h4')  # visible profile page

        list_of_articles = []
        articles = driver.find_elements_by_xpath('//div[@class="profile-page"]//h1')  # list of titles1
        for row in articles:
            list_of_articles.append(row.text + '\n')
        with open('articles.txt', 'w') as x:
            for item in list_of_articles:
                x.write(item)

            # search and delete article what title is "hello"
        element_click('//div[@class="container"]//ul/li[4]/a')  # user page
        wait_to('//*[@id="app"]/div/div[2]/div/div/div[1]/ul/li[1]/a')  # visible my articles
        
        time.sleep(10)
        find('//div[@class="article-preview"]/a[contains(@href,"hello")]').click()
        wait_to('//*[@id="app"]/div/div[1]/div/div/span/button')
        element_click('//*[@id="app"]/div/div[1]/div/div/span/button')  # delete article
        time.sleep(20)

        # # change user name
        element_click('//ul//a[contains(@href,"settings")]')  # settings
        wait_to('//*[@id="app"]/div/div/div/div/h1')  # visible 'Your Settings'
        user_name = find_and_clear('//*[@id="app"]/div/div/div/div/form/fieldset/fieldset[2]/input')
        user_name.send_keys("Pityu")  # username
        time.sleep(20)
        find('//*[@id="app"]/div/div/div/div/form/fieldset/button').click()  # Update settings button

        wait_to('/html/body/div[2]/div/div[2]')  # visible message

        if find('/html/body/div[2]/div/div[2]').text == 'Update successful!':
            element_click('/html/body/div[2]/div/div[3]/div/button')  # ok button
        wait_to('//*[@id="app"]/nav/div/ul/li[4]/a')  # visible user name
        time.sleep(20)
        assert find('//*[@id="app"]/nav/div/ul/li[4]/a').text == 'Pityu'
    finally:
        driver.close()
