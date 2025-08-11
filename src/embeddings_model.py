from langchain.vectorstores import FAISS
from settings import embedding_model


def embedding(embedding_model,document):

    vectorstore = FAISS.from_documents(document, embedding_model)
    vectorstore.save_local("faiss_job_index_miniLM")
    print("✅ Vector store with open-source embeddings created.")
    print(f"Number of vectors stored: {vectorstore.index.ntotal}")



def embedding_resume(resume):
    return  embedding_model.embed_documents([resume])[0]  # embedding for the single resume





