from resume_parser import resume_parsing , converting_resume_single_text

from jobs_scrapping import scraping_job,json_to_document

from settings import url,querystring

from embeddings_model import embedding,embedding_resume
from settings import embedding_model

from similarity_checks import similarity_checking
from langchain.vectorstores import FAISS

from chain import model_match_reason

resume_file_path = ''



parsed = resume_parsing(resume_file_path) # harcoded resume_path link needs to given for testing 
print("✅ Parsed JSON:\n", parsed)

text_output = converting_resume_single_text(parsed)
print("\n✅ Formatted Output:\n", text_output)

scraping= scraping_job(url,querystring)
print("\n Scraping Succesfull")

json_format=json_to_document(scraping)
print("\n Json to Documents is Succesfull")

do_embedding=embedding(embedding_model,json_format)

do_embedding_resume= embedding_resume(text_output)

# print(do_embedding_resume)


#Loading vector store  and performing similarity checks 
vectorstore = FAISS.load_local("faiss_job_index_miniLM", embedding_model, allow_dangerous_deserialization=True)
similarity_searching=similarity_checking(vectorstore,do_embedding_resume)
# print(similarity_searching)



final_result=model_match_reason(similarity_searching,text_output)
print(final_result)
print(len(final_result))



