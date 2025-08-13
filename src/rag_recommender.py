# src/rag_recommender.py
from textwrap import dedent

RECOMMEND_PROMPT = dedent("""
You are an expert career advisor.
You will receive:
- A USER PROFILE (possibly structured) and
- A list of CANDIDATE JOBS (each with title, organization, location(s), employment_type, seniority, and URL).

TASK:
1) Select the TOP {k} jobs that best match the user's skills, experience, preferences (job_type, location), and seniority.
2) Return a clear, numbered Markdown list. For EACH job include EXACTLY:
   - **Title**: <title>
   - **Company**: <organization>
   - **Location**: <locations_derived or 'N/A'>
   - **Employment Type**: <employment_type or 'N/A'>
   - **Seniority**: <seniority or 'N/A'>
   - **Link**: <url>
   - **Why this fits**: one concise sentence
   - **Highlights**:
     - 2–3 bullets tying the job to the user's profile

Keep it concise and useful. Do not invent missing data.
""").strip()

def format_user_profile(user_dict: dict) -> str:
    # user_dict may contain structured fields and/or full_text
    lines = []
    s = user_dict.get("structured", {})
    if s:
        lines.append(f"Skills: {', '.join(s.get('skills', [])) or 'N/A'}")
        lines.append(f"Experience: {s.get('experience','') or 'N/A'}")
        lines.append(f"Education: {s.get('education','') or 'N/A'}")
        lines.append(f"Location preference: {s.get('location','') or 'N/A'}")
        lines.append(f"Job type preference: {s.get('job_type','') or 'N/A'}")
    ft = user_dict.get("full_text", "")
    if ft:
        lines.append("\nFull resume text (for reference, keep private):\n" + ft[:1500])  # cap to avoid overloading
    return "\n".join(lines)

def format_candidate_jobs(cands: list[dict]) -> str:
    blocks = []
    for c in cands:
        raw = c.get("raw", c)  # ensure direct access if not wrapped
        blocks.append("\n".join([
            f"Title: {raw.get('title','')}",
            f"Company: {raw.get('organization','')}",
            f"Location(s): {raw.get('locations_derived','') or 'N/A'}",
            f"Employment Type: {raw.get('employment_type','') or 'N/A'}",
            f"Seniority: {raw.get('seniority','') or 'N/A'}",
            f"Link: {raw.get('url','') or 'N/A'}",
            "---"
        ]))
    return "\n".join(blocks)

def create_rag_prompt(user_dict: dict, candidate_jobs: list[dict], k: int = 5) -> str:
    return (
        RECOMMEND_PROMPT.format(k=k)
        + "\n\nUSER PROFILE:\n"
        + format_user_profile(user_dict)
        + "\n\nCANDIDATE JOBS:\n"
        + format_candidate_jobs(candidate_jobs)
    )
