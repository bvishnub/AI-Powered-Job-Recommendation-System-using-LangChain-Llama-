from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from settings import model
import os 

# print(resume_data)

def resume_parsing(tmp_file_path):
    loader=PyPDFLoader(file_path=tmp_file_path )
    docs=loader.load()
    resume_data= '\n'.join([doc.page_content for doc in docs])

    # Define the prompt template
    template = PromptTemplate.from_template(
        """
    You are a resume parser AI assistant.

    Extract the following information from the provided resume and return it in **valid JSON format only** (no extra text):
    - location (city, state/country if available)
    - job_title (list all job titles)
    - experience_years (approximate total)
    - skills (list all technical skills)
    - education (degree, major, and university)
    - certifications (if any)
    - preferred_job_type (e.g., Full-time, Internship, Remote)

    Resume:
    \"\"\"
    {resume_data}
    \"\"\"

    Respond with JSON only, no explanation or text outside the JSON block.
    """
    )
    
    parser= JsonOutputParser()

    resume_parsing_chain= template | model | parser

    return resume_parsing_chain.invoke({'resume_data':resume_data})



def converting_resume_single_text(resume_data):
    resume_text = (
        f"Location: {resume_data['location']}\n"
        f"Job Titles: {', '.join(resume_data.get('job_titles') or resume_data.get('job_title', []))}\n"
        f"Experience Years: {resume_data['experience_years']}\n"
        f"Skills: {', '.join(resume_data['skills'])}\n"
        f"Education: {', '.join(resume_data['education'])}\n"
        f"Certifications: {', '.join(resume_data['certifications'])}\n"
        f"Preferred Job Type: {resume_data['preferred_job_type']}"
    )
    return resume_text





    





