from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import subprocess
from ollama import chat
from ollama import ChatResponse
import random as r
import time

# Set paths
CHROMEDRIVER_PATH = "/etc/profiles/per-user/tufan/bin/chromedriver"
BRAVE_PATH = "/etc/profiles/per-user/tufan/bin/brave"

options = Options()
options.binary_location = BRAVE_PATH
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")

service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)
count=0
increment = 0
the_links = []
with subprocess.Popen(["typst","Toufiq Abir Farhan Resume(Master resume).md"], stdout=subprocess.PIPE, text=True) as proc:
  ret = proc.stdout.read()
  print(ret)
while True:
    try:
        if len(the_links) == 0:
         driver.get("https://jobs.sobeyscareers.com/search/?q=&q2=&alertId=&locationsearch=&title=&location=Halifax&department=&facility=")
        
        time.sleep(r.randint(1,3))
        the_links = driver.find_elements(By.XPATH, "//table[@id='searchresults']//tbody//a[@class]")
        print(f"links {len(the_links)} length") 
        print(the_links[count].text)
        
        driver.get(the_links[count].get_attribute("href"))
        time.sleep(r.randint(1,3))
        
        the_descriptions =  driver.find_elements(By.XPATH, "//span[@class='jobdescription']//div[1]")
        print(len(the_descriptions))
        # for elem in the_descriptions:
        #     for i in  elem.text.split("\n"):
        #         print(i + "Yo")
        
        unique = list(dict.fromkeys([i  for elem in the_descriptions for i in elem.text.split("\n") ]))
        for x  in unique:
            print(x)
        posting = ''''''.join(unique + "\n")
        print("This is the posting\n"+posting)

        #AI acceleration
        response: ChatResponse = chat(model='llama3.1', messages=[
        {
         'role': 'user',
         'content':'Based on the base resume \n'+ ret + '\n .Make a resume that only has relevant experiences from the base resume that matches the job posting responsiblities. Try to use job posting terminologies to pass the ATS in the new resume. Ignore any job posting that requires a license or more than 2 years of expereince. Here is the jobposting ' + posting,
        },
        ])
        #or access fields directly from the response object
        print(response.message.content)
        
        print("-"*50+"\nNext Post\n"+"-"*50+"\n")
        print(f"{count} post")
       
        time.sleep(r.randint(1,3))
        driver.back()

        # change to next posting
        increment = increment + 1
        count = (increment)*2
       
        if count == len(the_links):
           
            time.sleep(r.randint(1,3))
            break       
    except :
        print("Element not ready, retrying...")



# for elem in the_links:
#     print(elem.get_attribute("href") + elem.text)
    
#     count += 1
#     time.sleep(r.randint(1,3))
# response: ChatResponse = chat(model='llama3.2:3b', messages=[
#         {
#          'role': 'user',
#          'content':'Can you say what does this document say- ${cat Toufiq Abir Farhan Resume(Master resume).md }',
#         },
#         ])

# response: ChatResponse = chat(model='llama3.2:3b', messages=[
#   {
#     'role': 'user',
#     'content':'Go to this site' + the_links[1].get_attribute("href"),
#   },
# ])
#or access fields directly from the response object
#print(response.message.content)