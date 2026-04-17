from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random as r
import csv

CHROMEDRIVER_PATH = "/home/tufan/.nix-profile/bin/chromedriver"
BRAVE_PATH = "/home/tufan/.nix-profile/bin/brave"

options = Options()
options.binary_location = BRAVE_PATH
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--incognito")

service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

paginaton_url = 'https://www.careerbeacon.com/en/search/{0}?'
job_='Administrative+Assistant'
# List for storing unique job
list_new=[]
#going to the beacon website
print(paginaton_url.format(job_))
driver.get(paginaton_url.format(job_))
time.sleep(r.randint(20,25))
print("In site")

list_new = []

for page in range(40):
    print(f"\n--- Page {page+1} ---")

    job_list = driver.find_elements(
        By.XPATH,
        "//div[contains(@class,'serp_job_title') and contains(@class,'clickable')]/preceding-sibling::a"
    )

    for j in job_list:
        if j.get_attribute("href") not in list_new:
            list_new.append(j.get_attribute("href"))

    #print(list_new)

    expiry_dates = driver.find_elements(By.XPATH, "//div[contains(text(),'days')]")

    for job, date in zip(list_new, expiry_dates):
        print(job)
        print(date.text)

    print(len(job_list))
    print(len(expiry_dates))

    # Wait and go to next page
    time.sleep(r.randint(4, 7))

    try:
        next_page = driver.find_element(By.XPATH, '//a[@aria-label="Next page"]')
        next_page.click()
    except:
        print("No more pages")
        break

print(driver)

#take out links and expiry dates of posts
# job_list= driver.find_elements(By.XPATH,"//div[contains(@class,'serp_job_title') and contains(@class,'clickable')]/preceding-sibling::a")
# for j in job_list:
#     if j.get_attribute("href") not in list_new:
#         list_new.append(j.get_attribute("href"))        
# print(list_new)          
 
# expiry_dates = driver.find_elements(By.XPATH,"//div[contains(text(),'days')]")
# for job, date in zip(list_new,expiry_dates):
#  print(job)
#  print(date.text)
# # Wait and go to next page
# time.sleep(r.randint(4, 7))
# next_page = driver.find_element(By.XPATH,'//a[@aria-label="Next page"]').click()
# # time.sleep(r.randint(15,17));
# print(driver)
# print(len(job_list))
# print(len(expiry_dates))
