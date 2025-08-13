from langchain.vectorstores import FAISS
from embeddings_model import embedding_model

# Loading the vectorstore
vectorstore = FAISS.load_local("faiss_job_index_miniLM", embedding_model, allow_dangerous_deserialization=True)

def similarity_checking(vectorestore,resume_embedding):
    # This will return the most similar job documents to your resume
    search_results = vectorstore.similarity_search_by_vector(resume_embedding, k=10)
    print('Similarity Searching Completed') 
    return search_results





