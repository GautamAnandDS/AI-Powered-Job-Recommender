# app.py
import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

from src.fetch_jobs import get_jobs
from src.embeddings_store import VectorStore
from src.resume_parser import parse_resume
from src.rag_recommender import create_rag_prompt

load_dotenv()

GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-70b-8192")
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def groq_llm(prompt: str) -> str:
    resp = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": "You are an expert career advisor and concise writer."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.4,
        max_tokens=1200,
    )
    return resp.choices[0].message.content

# ---------- UI ----------
st.set_page_config(page_title="AI Job Recommender", layout="wide")
with open("styles.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("💼 AI-Powered Job Recommendation System")

# Sidebar controls
st.sidebar.header("Settings")
use_demo = st.sidebar.toggle("Use demo job dataset", value=True)
query = st.sidebar.text_input("Live API: title filter", "")
location_filter = st.sidebar.text_input("Live API: location filter", "")
topk_retrieve = st.sidebar.slider("Candidates to retrieve", 5, 30, 12)
topk_recommend = st.sidebar.slider("LLM top-K to show", 1, 10, 5)

mode = st.radio("Provide your profile by:", ["Manual input", "Upload resume (PDF)"])

user_dict = {"structured": {}, "full_text": ""}

if mode == "Manual input":
    skills = st.text_input("Skills (comma-separated)", "")
    experience = st.text_area("Experience summary (2–3 lines)", "")
    education = st.text_input("Highest education", "")
    pref_loc = st.text_input("Preferred location", "")
    job_type = st.selectbox("Job type preference", ["", "Full-time", "Part-time", "Internship", "Contract"])
    user_dict["structured"] = {
        "skills": [s.strip() for s in skills.split(",") if s.strip()],
        "experience": experience.strip(),
        "education": education.strip(),
        "location": pref_loc.strip(),
        "job_type": job_type,
    }
    # Also build a query text roughly equivalent to a resume summary
    user_dict["full_text"] = " ".join([
        "Skills:", skills,
        "Experience:", experience,
        "Education:", education,
        "Location:", pref_loc,
        "Preference:", job_type
    ]).strip()
else:
    uploaded = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])
    if uploaded:
        with st.spinner("Parsing your resume with LLM..."):
            parsed = parse_resume(uploaded, use_llm=True)
        user_dict = parsed
        st.success("Resume parsed successfully!")
        with st.expander("Preview extracted structure"):
            st.json(parsed.get("structured", {}))

if st.button("🔎 Get Recommendations", use_container_width=True):
    if not user_dict.get("full_text"):
        st.warning("Please provide your profile or upload a resume first.")
        st.stop()

    with st.spinner("Loading jobs and building the vector index..."):
        jobs = get_jobs(use_demo=use_demo, query=query, location=location_filter)
        vs = VectorStore()
        # For simplicity, rebuild index each run (okay for demo). Persist for prod.
        vs.build_from_jobs(jobs)

        # Use full resume/profile text for similarity
        candidates = vs.query(user_dict["full_text"], top_k=topk_retrieve)

    with st.spinner("Ranking with LLM..."):
        prompt = create_rag_prompt(user_dict, candidates, k=topk_recommend)
        llm_md = groq_llm(prompt)

    st.subheader("🎯 Recommendations")
    st.markdown(llm_md)

    # Optional: show the raw top-N similar jobs (pre-LLM) as cards
    with st.expander("Top similar jobs (pre-LLM)"):
        for c in candidates:
            raw = c.get("raw", c)
            st.markdown(f"""
<div class="job-card">
  <div class="job-title">{raw.get('title','')}</div>
  <div class="job-sub">{raw.get('organization','')}</div>
  <div class="badge">{raw.get('employment_type','') or 'N/A'}</div>
  <div class="badge">{raw.get('seniority','') or 'N/A'}</div>
  <div class="job-sub">{raw.get('locations_derived','') or ''}</div>
  <div class="job-link">🔗 <a href="{raw.get('url','')}" target="_blank">Job link</a></div>
</div>
""", unsafe_allow_html=True)
