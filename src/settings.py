from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os 
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS



# Chat Model
load_dotenv()
api_key_groq = os.getenv("GROQ_API_KEY")
os.environ["GROQ_API_KEY"] = api_key_groq
model = init_chat_model("llama3-8b-8192", model_provider="groq")


# Webscraping 
url = "https://jsearch.p.rapidapi.com/search"
job_title = 'Data Analyst OR Data Scientist OR AI Engineer'
querystring = {"query":job_title,"page":"1","num_pages":"3","country":"in","date_posted":"3days"}


# Embedding Model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")













