# src/rag_recommender.py
from textwrap import dedent

# Updated prompt for HTML output
RECOMMEND_PROMPT = dedent("""
You are an expert career advisor.
You will receive:
- A USER PROFILE (possibly structured)
- A list of CANDIDATE JOBS (each with title, organization, location(s), employment_type, seniority, and URL).

TASK:
1) Select the TOP {k} jobs that best match the user's skills, experience, preferences (job_type, location), and seniority.
2) Return **HTML only** (no Markdown, no explanations outside HTML).
3) For EACH job, create this structure:

<div class="job-card">
  <div class="job-title">[TITLE]</div>
  <div class="job-sub">[COMPANY]</div>
  <div class="badge">[EMPLOYMENT_TYPE]</div>
  <div class="badge">[SENIORITY]</div>
  <div class="job-sub">[LOCATION]</div>
  <div class="job-link">🔗 <a href="[URL]" target="_blank">Job link</a></div>
  <div class="job-details">
    <p><strong>Why this fits:</strong> [One concise sentence]</p>
    <ul>
      <li>[Highlight 1]</li>
      <li>[Highlight 2]</li>
      <li>[Highlight 3]</li>
    </ul>
  </div>
</div>

RULES:
- Replace placeholders with actual values from the selected jobs.
- Do not add extra fields or commentary.
- Keep “Why this fits” to 1 sentence.
- Keep Highlights to 2–3 short bullet points that directly match the user’s profile.
""").strip()


def format_user_profile(user_dict: dict) -> str:
    """Format the user profile into a readable text block."""
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
        lines.append("\nFull resume text:\n" + ft[:1500])  # cap for safety
    return "\n".join(lines)


def format_candidate_jobs(cands: list[dict]) -> str:
    """Format candidate jobs in plain text so LLM can understand them."""
    blocks = []
    for c in cands:
        raw = c.get("raw", c)
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
    """Create a prompt for the LLM with user profile and candidate jobs."""
    return (
        RECOMMEND_PROMPT.format(k=k)
        + "\n\nUSER PROFILE:\n"
        + format_user_profile(user_dict)
        + "\n\nCANDIDATE JOBS:\n"
        + format_candidate_jobs(candidate_jobs)
    )
