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
import requests
import asyncio
from capmonstercloudclient import CapMonsterClient, ClientOptions
from capmonstercloudclient.requests import RecaptchaV2ProxylessRequest
from twocaptcha import TwoCaptcha

website = 'https://www.mediacorp.sg/starawards/vote'
api_key = os.getenv('APIKEY_2CAPTCHA', '381978f518f47a2276c57ccb4e65427a')
solver = TwoCaptcha(api_key)

client_options = ClientOptions(api_key="1c067359c237fbbb8dae356f60829d08")
cap_monster_client = CapMonsterClient(options=client_options)

options = Options()
options.binary_location = os.environ.get("$GOOGLE_CHROME_BIN")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("detach", True)
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--headless')
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")

def vote(email,pass1):

    driver = webdriver.Chrome(options=options,executable_path="CHROMEDRIVER_PATH")

    try:
        driver.get(website)

        time.sleep(2)

        WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.ID,'mostpopularrising')))
                
        time.sleep(2)

        driver.execute_script("""document.querySelectorAll(('[data-voting-path="/votingapp/profiletab/MostPopularRisingStar2023"]'))[0].click();""")

        WebDriverWait(driver, 10).until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR,"iframe[name='vtg-frame']")))

        WebDriverWait(driver,10).until(expected_conditions.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[name='vtg-frame']"))) 

        WebDriverWait(driver,10).until(expected_conditions.element_to_be_clickable((By.ID,"vote_but_2388233")))

        driver.execute_script("document.getElementById('vote_but_2388233').click()")

        driver.execute_script('''document.querySelectorAll('[data-entryid="2388233"]')[0].click()''')
        time.sleep(2)

        WebDriverWait(driver,20).until(expected_conditions.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[id='iFrameResizer0']"))) 
        print("switched frame")
        time.sleep(1)
        print("keying in values")
        driver.execute_script("document.getElementById('loginemail').value='"+email+"';")
        time.sleep(1)
        driver.execute_script("document.getElementById('loginpassword').value='"+pass1+"';")
        time.sleep(1)
        driver.execute_script("document.getElementsByClassName('btn sign_in_btn')[0].click();")

        driver.switch_to.parent_frame()

        votes = 0
        while votes < 999999:
            try:

                async def solve_captcha():
                    return await cap_monster_client.solve_captcha(recaptcha2request)

                recaptcha2request = RecaptchaV2ProxylessRequest(websiteUrl="https://mediacorp.votigo.com/votingapp/profiletab/MostPopularRisingStar2023?hostingUrl=https%3A%2F%2Fwww.mediacorp.sg&x=1&vtgto=1D8nxawbIT5WS2S%2Fldb9JrJ0hEfhNWBw6lCQ8qHMLjX9sXluY0MmPjZgSuyj760z4umwsUaXumyBgM2I4vPrY%2B0J5NyENbBZvsn6%2FCk7atsvT5NpVqFgTWLF092wDL%2FJvbhxUF8Z1Zb%2FkPX%2B5znnXnaoWNkn81dnk0Y9IRSJP%2Bu8L%2FXWh0YejFcPMuR79uC7DB%2BqeXqJGaimBUjX7O3Ahpk2kP6fX8FNrZN6IVsaU%2FcHToQf0QPRMjfNW8QF0dHDuXmvqV53D6BpTdahjHRk8n9jeNH9R1UqJNkTXJlgaaidPxZu8NcrOcah034Y7faFQN35tDDferExNiToTjSzh3dffsY1KEa0YdvbwcfPaqbX9kXZF8nimdXX7POdo4ympGnG4FW92OGnzAgeNqaMcoRvfaAHgoCcllBhoUpagNQ70cYBP74c9%2Bhu0EdXcT%2F0mn46WSRWLZzWg6DTpQoRh9t8QYp%2Fk21I7AR4h3YZnMkSG4Jq19WYXwrMMhOb%2BTnpgvxZXEtlZEv%2FQaxpxCvmrw11eJVzATm%2BrXxDL2Za49vulFhkszLpYaQfEWZykAEM53naIlwk84LWzNqfLkwdZCcfjKa1t5XFs1%2FrXMCux6L8WJSKwjPd5KLPDHPkGsqZ&ogHostUrl=https%3A%2F%2Fwww.mediacorp.sg",
                                                                websiteKey="6LeC-gITAAAAAMsKNTNfV-bu7bBleRWo3jT8z8TA")

                responses = asyncio.run(solve_captcha())
                code = responses[('gRecaptchaResponse')]
                print(code)

                WebDriverWait(driver, 10).until(
                    expected_conditions.presence_of_element_located((By.ID, 'g-recaptcha-response')))

                driver.execute_script(
                "document.getElementById('g-recaptcha-response').innerHTML = " + "'" + code + "'")
                print('ok, code is injected')

                driver.execute_script('document.getElementsByName("captchaloginsubmit")[0].click();')

                print('voted')

                time.sleep(3)

                WebDriverWait(driver,10).until(expected_conditions.element_to_be_clickable((By.ID,"vote_but_2388233")))

                driver.execute_script("document.getElementById('vote_but_2388233').click()")

                driver.execute_script('''document.querySelectorAll('[data-entryid="2388233"]')[0].click()''')
                time.sleep(1)

                print('clicked captcha box, solving captcha..')

                votes+=1
                print(email+'> votes: '+str(votes))

            except Exception:
                print('voting failed. votes:'+str(votes))
                driver.refresh()
                continue

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