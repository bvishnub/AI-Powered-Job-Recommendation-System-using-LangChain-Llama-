import streamlit as st
from final_chain_link import final_chain
import tempfile
import os

st.set_page_config(page_title="AI Job Recommender", layout="wide")

# Centered title
st.markdown("<h1 style='text-align: center;'>AI-Powered Job Recommendation System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Upload your resume and enter your desired job title to get personalized recommendations 🚀</p>", unsafe_allow_html=True)

# Simple disclaimer
st.info("📋 **Please upload a valid resume file only** - The file should contain your work experience, education, skills, and contact information.")

resume_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
job_title = st.text_input("Enter desired job title or keywords (comma-separated)")

if st.button("Get Recommendations"):
    if resume_file and job_title.strip():
        try:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{resume_file.name.split('.')[-1]}") as tmp_file:
                tmp_file.write(resume_file.read())
                tmp_file_path = tmp_file.name
            
            # Process job title properly INSIDE the button click
            job_keywords = [keyword.strip() for keyword in job_title.split(',') if keyword.strip()]
            job_title_query = ' OR '.join(job_keywords) if job_keywords else job_title.strip()
            
            st.info(f"🔍 Searching for: **{job_title_query}**")
            
            # Pass the file path as resume_data with processing indicator
            with st.spinner("🤖 Analyzing your resume and finding matching jobs..."):
                results = final_chain.invoke(tmp_file_path)
            
            # Clean up temporary file
            os.unlink(tmp_file_path)
            
            st.success("✅ Recommendations generated successfully!")
            st.subheader("🎯 Top Job Recommendations")
            st.json(results)
            
        except Exception as e:
            st.error(f"❌ Error processing request: {str(e)}")
            if "token" in str(e).lower():
                st.error("🔤 Token limit exceeded. Try uploading a shorter resume.")
            elif "join" in str(e).lower():
                st.error("🔗 Data processing error. Please check your input format.")
                st.info("💡 Try entering job title without special characters or very long text.")
            
            # Clean up temporary file if error occurs
            if 'tmp_file_path' in locals() and os.path.exists(tmp_file_path):
                try:
                    os.unlink(tmp_file_path)
                except:
                    pass  # Ignore cleanup errors
    else:
        st.error("⚠️ Please upload a resume and enter a job title.")
