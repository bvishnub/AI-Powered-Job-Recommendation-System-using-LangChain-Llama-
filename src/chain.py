from langchain_core.output_parsers import JsonOutputParser
from settings import model
from langchain.prompts import PromptTemplate


def model_match_reason(search_results,extracted_data):

    parser=JsonOutputParser()

    prompt = PromptTemplate(
    template="""You are a strict job matching system. Your ONLY task is to return valid JSON - nothing else.

CRITICAL REQUIREMENTS:
- Output MUST be valid, parsable JSON only
- NO text before or after the JSON
- NO markdown formatting or code blocks
- NO explanations or commentary
- If no jobs qualify, return empty array: []

INPUT DATA:
Resume Skills/Experience: {extracted_data}
Available Jobs: {search_results}

MATCHING CRITERIA (ALL must be satisfied to include a job):
1. Job MUST explicitly match at least 3 skills/qualifications from the resume
2. Skills matching MUST be based on exact keywords or clear synonyms present in resume
3. Do NOT infer or assume skills not explicitly mentioned in resume
4. Do NOT include jobs with insufficient skill overlap
5. Each job MUST have clear justification using only resume content

REQUIRED OUTPUT FORMAT - Copy this structure exactly:
[
  {{
    "company_name": "exact company name from job posting",
    "job_title": "exact job title from posting", 
    "apply_link": "direct application URL",
    "match_justification": "List exactly 3+ matching skills from resume with brief explanation"
    "Similarity Score" : "Give the simalrity score as well"
  }}
]

VALIDATION RULES:
- Only include jobs that meet ALL matching criteria
- Match justification must reference specific skills/experience from resume
- All URLs must be complete and functional
- Maximum 5 jobs in output array
- Each field is mandatory - no null or empty values

JSON OUTPUT (no other text):""",
    input_variables=['search_results', 'extracted_data']
)


    
   

    chain= prompt | model | parser


    return chain.invoke({'search_results':search_results,'extracted_data': extracted_data})
    
