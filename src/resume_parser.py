# src/resume_parser.py
import json
import pdfplumber
from groq import Groq
import os

GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-70b-8192")
_groq_client = None

def _groq():
    global _groq_client
    if _groq_client is None:
        _groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    return _groq_client

def extract_text_from_pdf(file) -> str:
    """Extract raw text from a PDF file."""
    text = []
    with pdfplumber.open(file) as pdf:
        for p in pdf.pages:
            t = p.extract_text() or ""
            if t:
                text.append(t)
    return "\n".join(text).strip()

STRUCT_PROMPT = """You are a precise information extraction system.
Given the raw resume text below, extract a compact JSON object with keys:
- skills: array of short skill strings
- experience: brief free-text summary (2-3 lines max)
- education: brief free-text summary (1-2 lines)
- location: single city/region if available, else empty string
- job_type: optional preference if clearly stated (e.g., "Full-time", "Internship"), else empty string

Only output valid JSON. No extra commentary.

RESUME:
{resume_text}
"""

def llm_extract_structured(resume_text: str) -> dict:
    """Use LLM to extract structured resume info."""
    try:
        resp = _groq().chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": "Extract clean, compact JSON. No commentary."},
                {"role": "user", "content": STRUCT_PROMPT.format(resume_text=resume_text)}
            ],
            temperature=0.2,
            max_tokens=700,
        )
        content = resp.choices[0].message.content.strip()
        # Clean accidental code fences
        content = content.strip("`")
        content = content.replace("json\n", "").replace("JSON\n", "")
        data = json.loads(content)
        # Ensure minimal keys
        data.setdefault("skills", [])
        data.setdefault("experience", "")
        data.setdefault("education", "")
        data.setdefault("location", "")
        data.setdefault("job_type", "")
        return data
    except Exception as e:
        print(f"[Resume Parser] LLM extraction failed: {e}")
        return {"skills": [], "experience": "", "education": "", "location": "", "job_type": ""}

def parse_resume(file, use_llm: bool = True) -> dict:
    """
    Parse resume and return:
      - full_text: string for embeddings
      - structured: dict with keys (skills, experience, education, location, job_type)
    """
    txt = extract_text_from_pdf(file)
    structured = llm_extract_structured(txt) if use_llm else {
        "skills": [], "experience": "", "education": "", "location": "", "job_type": ""
    }
    return {"full_text": txt, "structured": structured}
