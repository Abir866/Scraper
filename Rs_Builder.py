from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from openai import OpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import  dotenv_values
from markdown import markdown
from weasyprint import HTML
import gradio as gr
import random as r
import time
# from functions import *

CHROMEDRIVER_PATH = "/home/tufan/.nix-profile/bin/chromedriver"
BRAVE_PATH = "/home/tufan/.nix-profile/bin/brave"

options = Options()
options.binary_location = BRAVE_PATH
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")

service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)


config = dotenv_values(".env")
api_key = config['OPENROUTER_API_KEY']

def process_resume (*inputs):
   with open(inputs[0], "r", encoding="utf-8") as file:
      read_resume = file.read()



   prompt_template = lambda read_resume, jd_input : f"""
   You are a professional resume optimization expert specializing in tailoring resumes to specific job descriptions. Your goal is to optimize my resume and provide actionable suggestions for improvement to align with the target role.

   ### Guidelines:
   1. **Relevance**:
      - Prioritize experiences, skills, and achievements **most relevant to the job description**.
      - Remove or de-emphasize irrelevant details to ensure a **concise** and **targeted** resume.
      - Limit work experience section to 4-5 most relevant roles
      - Limit bullet points under each role to 3-5 most relevant impacts
      - Try to cover 80% of the responsiblilities through transferable skills

   2. **Action-Driven Results**:
      - Use **strong action verbs** and **quantifiable results** (e.g., percentages, revenue, efficiency improvements) to highlight impact.

   3. **Keyword Optimization**:
      - Integrate **keywords** and phrases from the job description naturally to optimize for ATS (Applicant Tracking Systems).

   4. **Additional Suggestions** *(If Gaps Exist)*:
      - If the resume does not fully align with the job description, suggest:
      1. **Additional technical or soft skills** that I could add to make my profile stronger.
      2. **Certifications or courses** I could pursue to bridge the gap.
      3. **Project ideas or experiences** that would better align with the role.

   5. **Formatting**:
      - Output the tailored resume in **clean Markdown format**.
      - Include an **"Additional Suggestions"** section at the end with actionable improvement recommendations.

   ---

   ### Input:
   - **My resume**:
   {read_resume}

   - **The job description**:
   {jd_input}

   ---

   ### Output:
   1. **Tailored Resume**:
      - A resume in **Markdown format** that emphasizes relevant experience, skills, and achievements.
      - Incorporates job description **keywords** to optimize for ATS.
      - Uses strong language and is no longer than **one page**.

   2. **Additional Suggestions** *(if applicable)*:
      - List **skills** that could strengthen alignment with the role.
      - Recommend **certifications or courses** to pursue.
      - Suggest **specific projects or experiences** to develop.
   """

   prompt = prompt_template(read_resume, inputs[1])


   client = OpenAI(base_url="https://openrouter.ai/api/v1",api_key=api_key,)

   # make api call
   response = client.chat.completions.create(
      model="deepseek/deepseek-chat-v3-0324:free",
      messages=[
         {"role": "system", "content": "Expert resume writer"},
         {"role": "user", "content": prompt}
      ],
      temperature = 0.7
   )

   # extract response
   response_string = response.choices[0].message.content



   print(response_string)
   return



def create_app (posting):
   with gr.Blocks() as app:
      # create header and app description
      gr.Markdown("# Resume Optimizer 📄")
      gr.Markdown("Upload your resume, paste the job description, and get actionable insights!")

      # gather inputs
      with gr.Row():
         resume_input = gr.File(label="Upload Your Resume (.md)")
         jd_input = gr.Textbox(value= posting, label="Paste the Job Description Here", lines=9, interactive=True, placeholder="Paste job description...")
      run_button = gr.Button("Optimize Resume 🤖")

      # display outputs
      output_resume_md = gr.Markdown(label="New Resume")
      output_suggestions = gr.Markdown(label="Suggestions")

      # editing results
      output_resume = gr.Textbox(label="Edit resume and export!", interactive=True)
      export_button = gr.Button("Export Resume as PDF 🚀")
      export_result = gr.Markdown(label="Export Result")

      # Event binding
      run_button.click(process_resume, inputs=[resume_input, jd_input], outputs=[output_resume_md, output_resume, output_suggestions])
      export_button.click(export_resume, inputs=[output_resume], outputs=[export_result])

   # Launch the app
   app.launch()
   output_pdf_file = "resume_new.pdf"
   html_content = markdown(response_string)
   HTML(string=html_content).write_pdf(output_pdf_file)


def resume_read(resume_input):
   with open(resume_input, "r", encoding="utf-8") as file:
      read_resume = file.read(resume_input)
   return read_resume


def job_extraction():
   global the_links, count, increment
   while True:
      try:
         if len(the_links) == 0:
            driver.get("https://jobs.sobeyscareers.com/search/?q=&q2=&alertId=&locationsearch=&title=&location=Halifax&department=&facility=")

         time.sleep(r.randint(1,3))
         print("In site")

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
         create_app(posting)

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

count=0
increment = 0
the_links = []
job_extraction()
