from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import datetime
import time 
import random
import csv
import os
from twocaptcha import TwoCaptcha

website = 'https://www.mediacorp.sg/profile/login?redirect_url=%2Fstarawards%2Fvote'
api_key = os.getenv('APIKEY_2CAPTCHA', '381978f518f47a2276c57ccb4e65427a')
solver = TwoCaptcha(api_key)

options = Options()
options.binary_location = os.environ.get("$GOOGLE_CHROME_BIN")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("detach", True)
options.add_experimental_option('useAutomationExtension', False)
# options.add_argument('--headless')
# options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--no-sandbox")

def vote(email,pass1):

    driver = webdriver.Chrome(options=options,executable_path="CHROMEDRIVER_PATH")

    try:
        driver.get(website)

        driver.execute_script("document.getElementById('edit-email').value='"+email+"';")
        time.sleep(1)
        driver.execute_script("document.getElementById('edit-password').value='"+pass1+"';")
        time.sleep(1)
        driver.execute_script("document.getElementsByClassName('g-recaptcha login-captcha-form-submit')[0].click();")

        print('logged in')

        WebDriverWait(driver, 10).until(
        	expected_conditions.element_to_be_clickable((By.ID,'mostpopularrising')))
        
        time.sleep(1)

        driver.execute_script("""document.querySelectorAll(('[data-voting-path="/votingapp/profiletab/MostPopularRisingStar2023"]'))[1].click();""")

        WebDriverWait(driver, 10).until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR,"iframe[name='vtg-frame']")))

        WebDriverWait(driver,10).until(expected_conditions.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[name='vtg-frame']"))) 

        WebDriverWait(driver,10).until(expected_conditions.element_to_be_clickable((By.ID,"vote_but_2388233")))

        driver.execute_script("document.getElementById('vote_but_2388233').click()")
        time.sleep(1)

        driver.execute_script('''document.querySelectorAll('[data-entryid="2388233"]')[0].click()''')

        WebDriverWait(driver,10).until(
            expected_conditions.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,'iframe[title="reCAPTCHA"]')))

        checkbox = driver.find_element(By.CLASS_NAME, "recaptcha-checkbox-border")

        WebDriverWait(driver,10).until(
            expected_conditions.element_to_be_clickable((checkbox)))

        driver.execute_script('''document.getElementsByClassName('recaptcha-checkbox-border')[0].click()''')

        print('clicked captcha box, solving captcha..')

        result = solver.recaptcha(
            sitekey='6LeC-gITAAAAAMsKNTNfV-bu7bBleRWo3jT8z8TA',
            url='https://mediacorp.votigo.com/votingapp/profiletab/MostPopularRisingStar2023?hostingUrl=https%3A%2F%2Fwww.mediacorp.sg&x=1&vtgto=1D8nxawbIT5WS2S%2Fldb9JrJ0hEfhNWBw6lCQ8qHMLjX9sXluY0MmPjZgSuyj760z4umwsUaXumyBgM2I4vPrY%2B0J5NyENbBZvsn6%2FCk7atsvT5NpVqFgTWLF092wDL%2FJvbhxUF8Z1Zb%2FkPX%2B5znnXnaoWNkn81dnk0Y9IRSJP%2Bu8L%2FXWh0YejFcPMuR79uC7DB%2BqeXqJGaimBUjX7O3Ahpk2kP6fX8FNrZN6IVsaU%2FcHToQf0QPRMjfNW8QF0dHDuXmvqV53D6BpTdahjHRk8n9jeNH9R1UqJNkTXJlgaaidPxZu8NcrOcah034Y7faFQN35tDDferExNiToTjSzh3dffsY1KEa0YdvbwcfPaqbX9kXZF8nimdXX7POdo4ympGnG4FW92OGnzAgeNqaMcoRvfaAHgoCcllBhoUpagNQ70cYBP74c9%2Bhu0EdXcT%2F0mn46WSRWLZzWg6DTpQoRh9t8QYp%2Fk21I7AR4h3YZnMkSG4Jq19WYXwrMMhOb%2BTnpgvxZXEtlZEv%2FQaxpxCvmrw11eJVzATm%2BrXxDL2Za49vulFhkszLpYaQfEWZykAEM53naIlwk84LWzNqfLkwdZCcfjKa1t5XFs1%2FrXMCux6L8WJSKwjPd5KLPDHPkGsqZ&ogHostUrl=https%3A%2F%2Fwww.mediacorp.sg')

        code = result['code']

        print('code is '+ str(code))

        driver.switch_to.parent_frame()

        WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located((By.ID, 'g-recaptcha-response')))

        driver.execute_script(
        "document.getElementById('g-recaptcha-response').innerHTML = " + "'" + code + "'")
        print('ok, code is injected')

        driver.execute_script('document.getElementsByName("captchaloginsubmit")[0].click();')

        print('voted once')

        time.sleep(3)
        driver.execute_script("document.getElementById('vote_but_2388233').click()")

        try:
            WebDriverWait(driver, 3).until(expected_conditions.alert_is_present(),
                                           'Timed out waiting for PA creation ' +
                                           'confirmation popup to appear.')

            alert = driver.switch_to.alert
            alert.accept()
            print("alert accepted")
        except:
            print("no alert")

        time.sleep(1)
        driver.execute_script('document.getElementsByName("captchaloginsubmit")[0].click();')

        print('voted twice')

        time.sleep(1)
        driver.execute_script("document.getElementById('vote_but_2388233').click()")
        time.sleep(1)
        driver.execute_script('document.getElementsByName("captchaloginsubmit")[0].click();')

        print('voted 3 times')

        time.sleep(1)
        driver.execute_script("document.getElementById('vote_but_2388233').click()")
        time.sleep(1)
        driver.execute_script('document.getElementsByName("captchaloginsubmit")[0].click();')

        print('voted 4 times')

        with open(os.path.realpath('paper.csv'), 'a', encoding='UTF8',newline='') as f:
            # create the csv writer
            writer = csv.writer(f)
            current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            writer.writerow([current_time,email,pass1])

        print('voted successfully')
        
        driver.quit()

    except Exception as e:
        with open(os.path.realpath('empty.csv'), 'a', encoding='UTF8',newline='') as f:
            # create the csv writer
            writer = csv.writer(f)
            current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            writer.writerow([current_time,email,pass1])
        print(e)
        print('voting failed')
        driver.quit()

    else:
        print('reached else statement, closing driver..')
        driver.quit()