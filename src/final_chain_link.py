from langchain.schema.runnable import RunnableLambda, RunnableMap
from langchain.vectorstores import FAISS
from resume_parser import resume_parsing, converting_resume_single_text
from jobs_scrapping import scraping_job, json_to_document
from embeddings_model import embedding, embedding_resume
from similarity_checks import similarity_checking
from chain import model_match_reason
from settings import get_query, embedding_model


# Create runnables

parse_resume = RunnableLambda(lambda file_path: resume_parsing(file_path))
convert_resume_text = RunnableLambda(lambda parsed: converting_resume_single_text(parsed))
embed_resume_text = RunnableLambda(lambda text: embedding_resume(text))
scrape_jobs = RunnableLambda(lambda job_title: scraping_job(*get_query(job_title)))
jobs_to_docs = RunnableLambda(lambda jobs: json_to_document(jobs))
embed_jobs = RunnableLambda(lambda docs: embedding(embedding_model, docs))
similarity_search = RunnableLambda(
    lambda resume_emb: similarity_checking(
        FAISS.load_local(
            "faiss_job_index_miniLM",
            embedding_model,
            allow_dangerous_deserialization=True
        ),
        resume_emb
    )
)
match_reasoning = RunnableLambda(lambda data: model_match_reason(data["search_results"], data["resume_text"]))

# Final chain

final_chain = RunnableMap({
    "resume_text": (
        RunnableLambda(lambda d: d["file_path"])
        | parse_resume
        | convert_resume_text
    ),
    "resume_emb": (
        RunnableLambda(lambda d: d["file_path"])
        | parse_resume
        | convert_resume_text
        | embed_resume_text
    ),
    "scraped_jobs": (
        RunnableLambda(lambda d: d["job_title"])
        | scrape_jobs
        | jobs_to_docs
        | embed_jobs
    )
}) | RunnableMap({
    "resume_text": RunnableLambda(lambda d: d["resume_text"]),
    "resume_emb": RunnableLambda(lambda d: d["resume_emb"]),
    "search_results": RunnableLambda(
        lambda d: similarity_checking(
            FAISS.load_local(
                "faiss_job_index_miniLM",
                embedding_model,
                allow_dangerous_deserialization=True
            ),
            d["resume_emb"]
        )
    )
}) | match_reasoning
