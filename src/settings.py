from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os 
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS



# Chat Model
load_dotenv()
api_key_gemini = os.getenv("GEMINI_API_KEY")  
os.environ["GEMINI_API_KEY"] = api_key_gemini
model = init_chat_model("gemini-2.5-flash", model_provider="google_genai", api_key=api_key_gemini)



# # Chat Model
# load_dotenv()
# api_key_groq = os.getenv("GROQ_API_KEY")
# os.environ["GROQ_API_KEY"] = api_key_groq
# model = init_chat_model("llama3-8b-8192", model_provider="groq")




# Function to get querystring dynamically
def get_query(job_title):
    url = "https://jsearch.p.rapidapi.com/search"
    query_params= {
            "query": job_title,
            "page": "1",
            "num_pages": "3",
            "country": "in",
            "date_posted": "3days"
        }
    return url ,query_params





# Embedding Model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")













