# src/fetch_jobs.py
import os
import json
import requests

def load_demo_jobs(path="data/jobs_api.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def fetch_jobs_live(query: str = "", location: str = ""):
    """
    RapidAPI LinkedIn Jobs mirror.
    """
    host = os.getenv("RAPIDAPI_HOST")
    key = os.getenv("RAPIDAPI_KEY")
    if not host or not key:
        raise EnvironmentError("RAPIDAPI_HOST or RAPIDAPI_KEY not set")

    # Example endpoint (adjust if your plan uses a different one)
    url = f"{host.rstrip('/')}/active-jb-24h"
    headers = {
        "X-RapidAPI-Key": key,
        "X-RapidAPI-Host": host.replace("https://", "").replace("http://", ""),
    }
    params = {"title_filter": query, "location_filter": location}
    r = requests.get(url, headers=headers, params=params, timeout=15)
    r.raise_for_status()
    return r.json()

def preprocess_jobs(jobs):
    """
    Keep only the fields you specified, and normalize to strings.
    """
    processed = []
    for job in jobs:
        processed.append({
            "id": job.get("id"),
            "title": job.get("title"),
            "organization": job.get("organization"),
            "employment_type": ", ".join(job.get("employment_type", [])) if isinstance(job.get("employment_type"), list) else (job.get("employment_type") or ""),
            "url": job.get("url"),
            "locations_derived": ", ".join(job.get("locations_derived", [])) if isinstance(job.get("locations_derived"), list) else (job.get("locations_derived") or ""),
            "linkedin_org_description": job.get("linkedin_org_description", ""),
            "seniority": job.get("seniority", "")
        })
    return processed

def get_jobs(use_demo=True, query="", location=""):
    jobs = load_demo_jobs() if use_demo else fetch_jobs_live(query=query, location=location)
    return preprocess_jobs(jobs)
