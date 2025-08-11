import requests
from dotenv import load_dotenv
import os 
from settings import url,querystring,job_title
from langchain.schema import Document


load_dotenv()

def scraping_job(url,querystring):
    api_key = os.getenv("RAPIDAPI_KEY")
    api_host = os.getenv("RAPIDAPI_HOST")
    
    headers = {
        "x-rapidapi-key":api_key ,
        "x-rapidapi-host": api_host
    }
    
    response = requests.get(url, headers=headers, params=querystring)
    results= response.json()
    result=results['data']
    print(result[0])

    return result



# Converting Json file fetched from web scraping to Document 



def json_to_document(result):
    documents = []
    
    for job in result:
        text = (
            f"Job Title: {job.get('job_title', '')}\n"
            f"Company: {job.get('employer_name', '')}\n"
            f"Location: {job.get('job_city', '')}, {job.get('job_country', '')}\n"
            f"Description: {job.get('job_description', '')}\n"
            f"Qualifications: {job.get('job_highlights', {}).get('Qualifications', '')}\n"
        )
        
        metadata = {
            "job_id": job.get("job_id", ""),
            "company": job.get("employer_name", ""),
            "application_link" : job.get("job_apply_link", ""),
            "title": job.get("job_title", "")
        }
        
        documents.append(Document(page_content=text, metadata=metadata))
    
    return documents




    