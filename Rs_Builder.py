from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from openai import OpenAI
from langchain.prompts import PromptTemplate
import subprocess
from dotenv import  dotenv_values
from markdown import markdown
from weasyprint import HTML
import gradio as gr
import random as r
import time
import pandas as pan
# from functions import *
# Setting up the drver and broowser communication with special options
CHROMEDRIVER_PATH = "/home/tufan/.nix-profile/bin/chromedriver"
BRAVE_PATH = "/home/tufan/.nix-profile/bin/brave"

options = Options()
options.binary_location = BRAVE_PATH
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--incognito")

# service = Service(CHROMEDRIVER_PATH)
# driver = webdriver.Chrome(service=service, options=options)
#Global variables
global the_links, increment, count
count = 2

config = dotenv_values(".env")
api_key = config['OPENROUTER_API_KEY']

# Read the job links from csv file
csv_File = pan.read_csv("jobs.csv")

# optimize resume
def process_resume (*inputs):
   with open(inputs[0], "r", encoding="utf-8") as file:

      read_resume = file.read()
   system_prompt_template =  f'''

   You are a resume generator that gives expereinces in typst format following a particular
   structure as will be given in output format example. You will be using 3 to 4 bullet points from relevant job titles in work history as content of the output that are close to the job posting points
   based on semantic closeness, try using job posting keywords for bullets that are already
   similar to increase ATS score. Make sure the expeeinces are sorted from most recent to later

   Always separate the typst structure uing TOU from the rest of the response.
   Example of an Input pompt and its out put :
   Input - Use the work history below
   Customer Service Representative Halifax, NS
   Atlantic Superstore Sep 2025 - Present
   • Provide support to customer during solving product exchange issues by leadng converstation following a flow guide to
   ask relevant questions increasing efficiency to properly complete resolution procedure while adpating tone accordingly
   to make the interaction more humanly
   • Sold wide range of products from processed , fresh, frozen food items by understanding customer's travel needs and
   connecting the prodcct with features that stasfies the requirements thus providng personalizing customer experience
   • Offer additional complimentary products as recommendations that can improve the experience with the orginal
   product whereas keeping it customer's budget friendly

   to give me expereinces in typst structure that aligns with the job posting , as follows
   The Admitting Clerk ensures that the principles and practices that guide NSHA such as the mission
   vision, values,expected behaviors, the leadership philosophy, organizational health, population health, ethics, safety, quality, partnerships and Interprofessional collaboration are integrated within the services they provide and through the messages they deliver. About You We would love to hear from you if you have the following: Graduate of a recognized office administration program or equivalent required Completion of medical terminology certificate required Minimum of one year recent related clerical experience which includes utilizing medical terminology,
   patientbooking systems, health care systems and processes Microsoft Office expertise
   in Word, Excel and Outlook required. Clerical experience related to patient booking using Community Wide Scheduling required

   Output
   resume.experience(
     company: "Saint Mary's University",
     location: "Halifax, NS",
     role: "Computing Science Tutor",
     start: "Sep 2023",
     end: "Jun 2024",
     points: (
       "Clarified student needs by asking guided questions and identifying the purpose of each request, ensuring accurate and personalized support.",
       "Tracked and followed up on open issues by maintaining detailed records and checking resolution status, ensuring no requests were left unresolved.",
       "Managed scheduling of multiple sessions by coordinating availability through calls and planning Microsoft Teams meetings in advance, ensuring smooth session flow.",

   '''

   prompt_template = lambda read_resume, jd_input : f"""
  Review the resume content I will provide


   Your task is to extract only the experiences that align with an Administrative Assistant role (such as admin assistant in healthcare or similar environments) and rewrite them clearly and concisely.

   Do not add any new skills or embellish anything. Only use what already exists in the resume.

   Each bullet point must:

   Show the skill
   Explain how it was performed
   Explain why it was done (impact or purpose)
   Keep the original tone natural and authentic
   Be concise and avoid redundancy

   Output the experience section in Typst format using this structure:

   resume.experience(
   company: "...",
   location: "...",
   role: "...",
   start: "...",
   end: "...",
   points: (
   "...",
   "...",
   ),
   ),

   Group bullets under their correct jobs from the resume.

   After generating the Typst section, clearly separate it from the rest of your response

   Here is the resume of my entire Work history {read_resume}
   and here is the job description {jd_input}

   """

   prompt = prompt_template(read_resume, inputs[1])


   client = OpenAI(base_url="https://openrouter.ai/api/v1",api_key=api_key,)

   # make api call
   response = client.chat.completions.create(
      model="openai/gpt-oss-120b:free",
      messages=[
         {"role": "system", "content": system_prompt_template},
         {"role": "user", "content": prompt}
      ],
      temperature = 0.7
   )

   # extract response
   response_string = response.choices[0].message.content

   full_resume = """
   #import "../lib/resume.typ"
   
   // Resume
   
   #resume.full(
     head: resume.header(
       name: "Toufiq Abir Farhan Tufan",
       address: "B3L 1J8, Halifax, NS, Canada",
       links: (
         link("tel:+1 (902) 817-8338"),
         link("mailto:toufiqabir5@gmail.com"),
         link("https://abir866.github.io/my-porfolio/", "my-porfolio"),
         link("https://www.linkedin.com/in/toufiq-abir-farhan/", "linkedin.com/in/toufiq-abir-farhan"),
         link("https://github.com/Abir866/", "github.com/Abir866"),
       ),
     ),
     profile: "Self-motivated, organized administrative assistant with over 1 year of experience preparing and organizing documents, maintaining accurate records, and communicating through email and phone, scheduling appointments in a fast-paced customer focused environment. Welcoming and appreciative personality with the ability to adapt according to required organization standard procedures and policies. Demonstrated ability to be detail-oriented in analysing information and ensuring integrity. Always take a company-first approach and maintain confidentiality of proprietary information. Confident in managing time to be able to multi-task various operational procedures maintaining quality that aligns with company needs and values ",
   
   education: (
     resume.education(
       institution: "Saint Mary's University",
       location: "Halifax, NS",
       program: "Bachelor of Science",
       major: "Computer Science",
       start: "Sep 2020",
       end: "May 2024",
       courses: (
         "Intro to Computer Applications",
         "Data Management",
         "Microeconomics",
       ),
     ),
   ),
   experience: (
   resume.experience(
   company: "Concentrix",
   location: "Halifax, NS",
   role: "Advisor II",
   start: "Mar 2026",
   end: "Current",
   points: (
     "Assisted users with non-routine issues related to travel products and services timely maximizing customer satisfaction and retention.",
     "Diagnosed and resolved customer problems while meeting service KPIs",
     "Resolve travel bookings, ticket refund and flight re-scheduling concerns of customers facilitating a smooth experience",
     "Build strong relationships with customers through empathy towards different needs to adopt personalizing the solutions ",
     "Logged calls and maintained accurate case notes in tracking systems"
   
   ),
   ),
   """ + response_string  + """
   ),
   skills-dict: (
     "Core Skills": (
       "Email & Phone Correspondence",
       "Friendly and Professional Behaviour",
       "Maintain product knowledge base",
       "Adherence to standard scripts",
       "Product recommendations",
       "Complimentary sales",
       "Customer Service",
       "Relationship building",
       "Personal branding",
       "Automated Content updates"
     ),
     "Tools": (
       "Microsoft 365(Excel, Access database)",
       "Content Management Software",
       "Windows",
     ),
     "Strengths": (
       "Situational Awareness",
       "Calm Under Pressure",
       "Professional Presence",
       "Observational Skills",
       "Accountability",
     ),
    ),
   )
   """

   print(response_string)
   return full_resume

def export_resume(new_resume):
    """
    Convert a markdown resume to PDF format and save it.

    Args:
        new_resume (str): The resume content in markdown format

    Returns:
        str: A message indicating success or failure of the PDF export
    """
    with open("src/resume_starter.typ",'w') as writer:
        writer.write(new_resume)
    # try:
    #     # save as PDF
    #     output_pdf_file = "resumes/resume_new.pdf"

    #     # Convert Markdown to HTML
    #     html_content = markdown(new_resume)

    #     # Convert HTML to PDF and save
    #     HTML(string=html_content).write_pdf(output_pdf_file, stylesheets=['resumes/style.css'])

    #     return f"Successfully exported resume to {output_pdf_file} 🎉"
    # except Exception as e:
    #     return f"Failed to export resume: {str(e)} 💔"
    with subprocess.Popen(["typst","compile","--root", ".", "./src/resume_starter.typ"], stdout=subprocess.PIPE, text=True) as proc:
        time.sleep(2)
        proc.kill()
    return f'Successfully exported resume {new_resume}'



def resume_read(resume_input):
   with open(resume_input, "r", encoding="utf-8") as file:
      read_resume = file.read(resume_input)
   return read_resume


def job_extraction():

   
   # Define job and location search keywords
   # job_search_keyword = ['Data+Scientist', 'Business+Analyst', 'Data+Engineer',
   #                       'Python+Developer', 'Full+Stack+Developer',
   #                       'Machine+Learning+Engineer']
   # Define job and location search keywords
   # location_search_keyword = ['New+York', 'California', 'Washington']
   # Finding location, position, radius=35 miles, sort by date and starting page
   # paginaton_url = 'https://www.careerbeacon.com/en/search/{0}?'
   # job_='Administrative+Assistant'
   # #next_page = 1
   global count

   #Extract job details in the posting

   if csv_File.at[count,'Applied']== False:
          job_link = csv_File.at[count,'Job Link']
          csv_File.at[count,'Applied'] = True
          count = count + 1
          print(job_link)
   else:
           while(csv_File.at[count,'Applied'] != False):
              count = count + 1
           job_link = csv_File[count,'Job Link']
           csv_File.at[count,'Applied'] = True


   service = Service(CHROMEDRIVER_PATH)
   driver = webdriver.Chrome(service=service, options=options)
   driver.get(job_link)
   container = WebDriverWait(driver, 20).until(
           EC.presence_of_element_located((By.CSS_SELECTOR, "section.details > div"))
       )
   elements = container.find_elements(By.XPATH, ".//*[contains(text(),' ')]")
   return "\n".join([line_element.get_attribute("textContent") for line_element in elements])
       # job_post = driver.get(each_link)
       # job_details = driver.find_elements(By.XPATH,"//section[contains(@class,'details')]/div//p[contains(text(),' ')] and li[contains(text(),' ')]")
       # print(*[line_element.text for line_element in job_details], sep="\n" )
       # time.sleep(r.randint(4,5))
       #
       # 1. Navigate to the Indeed login page




       # 4. Enter Password (Wait for field to appear after clicking continue)
   # password_field=driver.find_element(By.NAME, "__password")
   # password_field.send_keys("your_password")

       # Wait for the dashboard to load to verify success



          # 2. Enter Email

   # email_field = driver.find_element(By.NAME, "__email")
   # email_field.send_keys("dolon2106000@gmail.com")

          # 3. Click Continue (Indeed often uses a multi-step login)
   # continue_button = driver.find_element(By.XPATH, "//button[@type='submit']")

   # continue_button.click()
   # time.sleep(r.randint(55,60))
            # driver.get("https://jobs.sobeyscareers.com/search/?q=&q2=&alertId=&locationsearch=&title=&location=Halifax&department=&facility=")


#Code to extract listings from job page


   # job_list= driver.find_elements(By.CSS_SELECTOR,'a.serp_job_title')
   # for job in job_list:
   #     print(job.get_attribute("href"))
   # time.sleep(r.randint(5, 7))
   # next_page = driver.find_element(By.XPATH,'//a[@aria-label="Next page"]').click()
   # time.sleep(r.randint(15,17));
   # print(driver)
   # print(len(job_list))



 #next_page = driver.find_element(By.XPATH,'//a[@aria-label="Next page"]').click()

    #Maximum number of pages for this section



   # print('Max Iterable Pages for this search:',max_iter_pgs)

   # for i in range(0, max_iter_pgs):
   #     driver.get(paginaton_url.format(job_,location,i*10))


   #     time.sleep(r.randint(2, 4))

   #     job_page = driver.find_element(By.ID,"mosaic-jobResults")
   #     jobs = job_page.find_elements(By.CLASS_NAME,"job_seen_beacon") # return a list

   #     for jj in jobs:
   #         job_title = jj.find_element(By.CLASS_NAME,"jobTitle")

   #         job_title.click()

   #         time.sleep(r.randint(3, 5))

   #         try:
   #                     job_description_list.append(driver.find_element(By.ID,"jobDescriptionText").text)

   #         time.sleep(r.randint(7,10));  #                     job_description_list.append(None)
         # the_links = driver.find_elements(By.XPATH, "//table[@id='searchresults']//tbody//a[@class]")
         # print(f"links {len(the_links)} length")
         # print(the_links[count].text)

         # driver.get(the_links[count].get_attribute("href"))
         # time.sleep(r.randint(1,3))

         # the_descriptions =  driver.find_elements(By.XPATH, "//span[@class='jobdescription']//div[1]")
         # print(len(the_descriptions))
         # # for elem in the_descriptions:
         # #     for i in  elem.text.split("\n"):
         # #         print(i + "Yo")

         # # unique = list(dict.fromkeys([i  for elem in the_descriptions for i in elem.text.split("\n") ]))
         # # for x  in unique:
         # #       print(x)
         # # posting = ''''''.join(x + "\n")
         # # print("This is the posting\n"+posting)
         # create_app(posting)

         # print("-"*50+"\nNext Post\n"+"-"*50+"\n")
         # print(f"{count} post")

         # time.sleep(r.randint(1,3))
         # driver.back()

         # # change to next posting
         # increment = increment + 1
         # count = (increment)*2

         # if count == len(the_links):

         #       time.sleep(r.randint(1,3))
         #       break

         # print("Element not ready, retrying...")
def previous_job():
    global count
    csvFile 
    count = count - 1
    return "Clicked!"
def create_app ():
   with gr.Blocks() as app:
      # create header and app description
      gr.Markdown("# Resume Optimizer 📄")
      gr.Markdown("Upload your resume, paste the job description, and get actionable insights!")
      with gr.Row():
          grab_button = gr.Button("Grab resume")
          uncheck_button = gr.Button("Check as Applied")
      # gather inputs
      with gr.Row():
         resume_input = gr.File(label="Upload Your Resume (.pdf)")
         jd_input = gr.Textbox(label="Paste the Job Description Here", lines=9, interactive=True, placeholder="Paste job description...")
      run_button = gr.Button("Optimize Resume 🤖")

      # display outputs
      # output_resume_typ = gr.Markdown(label="New Resume")
      # output_suggestions = gr.Markdown(label="Suggestions")

      # editing results
      output_resume = gr.Textbox(label="Edit resume and export!", interactive=True)
      export_button = gr.Button("Export Resume as PDF 🚀")
      export_result = gr.Markdown(label="Export Result")
      uncheck_button.click(previous_job,outputs=[output_resume])

      # Event binding
      grab_button.click(job_extraction, outputs=[jd_input])
      run_button.click(process_resume, inputs=[resume_input, jd_input], outputs=[output_resume])
      export_button.click(export_resume, inputs=[output_resume], outputs=[export_result])
      
   # Launch the app
   app.launch()
   # output_pdf_file = "resume_new.pdf"
   # html_content = markdown(response_string)
   # HTML(string=html_content).write_pdf(output_pdf_file)
create_app()

