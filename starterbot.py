from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import rungit
import time 
import csv
import numpy as np
import pandas as pd
import os

options = Options()
options.binary_location = os.environ.get("$GOOGLE_CHROME_BIN")
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument('--headless')
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")

df = pd.read_csv('MOCK_DATA.csv',header=0,names=['first_name','last_name','email','dob'])

for index, row in df.iterrows():
	driver = webdriver.Chrome(options=options,executable_path="CHROMEDRIVER_PATH")
	try:
		driver.get('https://www.mediacorp.sg/profile/register')
		print(str(row['email']))

		time.sleep(2)
		driver.execute_script("document.getElementById('edit-first-name').value='"+str(row['first_name'])+"'")
		driver.find_element(By.ID,'edit-first-name').click()

		driver.execute_script("document.getElementById('edit-last-name').value='"+str(row['last_name'])+"'")
		driver.find_element(By.ID,'edit-last-name').click()

		driver.execute_script("document.getElementById('edit-email').value='"+str(row['email'])+"'")
		driver.find_element(By.ID,'edit-email').click()

		driver.execute_script("document.getElementById('edit-password').value='12341234@'")
		driver.find_element(By.ID,'edit-password').click()

		driver.execute_script("document.getElementById('edit-confirm-password').value='12341234@'")


		Select(driver.find_element(By.ID,'edit-gender')).select_by_value('male')
		driver.execute_script("document.getElementById('edit-dob').value='"+str(row['dob'])+"'")
		
		time.sleep(3)
		driver.find_element(By.ID,'edit-confirm-password').click()
		driver.find_element(By.ID,'edit-dob').click()

		driver.execute_script("document.getElementsByClassName('form-item__label')[6].click()")
		driver.execute_script("document.getElementById('edit-terms-condition').click()")
		time.sleep(2)

		driver.execute_script("document.getElementsByClassName('g-recaptcha register-captcha-form-submit')[0].click()")
		time.sleep(5)

		if driver.current_url == 'https://www.mediacorp.sg/':
			rungit.append_this(str(row['email']),'12341234@')
			print("new acct created")
			continue
		else:
			print("sth went wrong, sobs")
			continue
	except:
		print("got error")
		continue

	driver.quit()

