from langchain.schema.runnable import RunnableLambda, RunnableMap, RunnableSequence
from langchain.vectorstores import FAISS
from resume_parser import resume_parsing, converting_resume_single_text
from jobs_scrapping import scraping_job, json_to_document
from embeddings_model import embedding, embedding_resume
from similarity_checks import similarity_checking
from chain import model_match_reason
from settings import url, querystring, embedding_model

# Step 1: Resume parsing
parse_resume = RunnableLambda(lambda file_path: resume_parsing(file_path))

# Step 2: Convert parsed JSON to text
convert_resume_text = RunnableLambda(lambda parsed: converting_resume_single_text(parsed))

# Step 3: Embed resume
embed_resume_text = RunnableLambda(lambda text: embedding_resume(text))

# Step 4: Scrape jobs
scrape_jobs = RunnableLambda(lambda _: scraping_job(url, querystring))

# Step 5: Convert jobs to documents
jobs_to_docs = RunnableLambda(lambda jobs: json_to_document(jobs))

# Step 6: Embed jobs
embed_jobs = RunnableLambda(lambda docs: embedding(embedding_model, docs))

# Step 7: Load vectorstore & similarity check
similarity_search = RunnableLambda(
    lambda resume_emb: similarity_checking(
        FAISS.load_local("faiss_job_index_miniLM", embedding_model, allow_dangerous_deserialization=True),
        resume_emb
    )
)

# Step 8: Match reason
match_reasoning = RunnableLambda(lambda sim_results: model_match_reason(sim_results, "resume_text_placeholder"))

# Build final chain
final_chain = RunnableSequence(
    parse_resume
| convert_resume_text
    | RunnableMap({
        "resume_emb": embed_resume_text,
        "scraped_jobs": scrape_jobs
    })    
    | RunnableLambda(lambda d: {
        "resume_emb": d["resume_emb"],
        "job_emb": embedding(embedding_model, json_to_document(d["scraped_jobs"]))
    })
    | RunnableLambda(lambda d: similarity_checking(
        FAISS.load_local("faiss_job_index_miniLM", embedding_model, allow_dangerous_deserialization=True),
        d["resume_emb"]
    ))
    | match_reasoning
)

