# main.py
"""
Plain-text pipeline steps that return human-readable sections
and a single orchestrator returning all intermediate outputs.

- Extract requirements from JD
- Parse resume (PDF or text fallback)
- Match requirements vs resume
- Company research (web)
- Tailored resume draft (text)
- Cover letter draft (text)
- Snapshot to JSONL for audit

Dependencies:
  - PyPDF2
  - openai (for web tool) and your MLService abstraction
"""

import io
import json
import datetime
from typing import Optional, Dict, Any

from PyPDF2 import PdfReader

from ml_service import MLService
from prompts import (
    EXTRACT_REQUIREMENTS_PROMPT,
    MATCH_REQUIREMENTS_PROMPT,
    COMPANY_RESEARCH_PROMPT,
    TAILOR_RESUME_PROMPT,
    COVER_LETTER_PROMPT,
)

from openai import OpenAI
from constants import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

# Model selection (adjust as needed)
EXTRACTION_MODEL = "gpt-4o-mini"
MATCH_MODEL = "gpt-4o-mini"
RESUME_MODEL = "gpt-4o"
COVER_LETTER_MODEL = "gpt-4o-mini"
WEB_MODEL = "gpt-4.1"  # supports web_search_preview

ml_service = MLService(EXTRACTION_MODEL)

# ---------- helpers ----------

def _now_iso() -> str:
    return datetime.datetime.now().isoformat(timespec="seconds")

def save_snapshot_jsonl(snapshot: Dict[str, Any], path: str = "runs_log.jsonl") -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(snapshot, ensure_ascii=False) + "\n")

def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(pdf_bytes))
    chunks = []
    for page in reader.pages:
        chunks.append(page.extract_text() or "")
    return "\n".join(chunks).strip()

# ---------- steps ----------

def extract_requirements_from_jd(job_description: str) -> Dict[str, Any]:
    prompt = EXTRACT_REQUIREMENTS_PROMPT.format(job_description=job_description.strip())
    messages = [{"role": "user", "content": prompt}]
    resp, meta = ml_service.call_llm(
        messages=messages,
        model=EXTRACTION_MODEL,
        call_type="extract_requirements",
        max_tokens=1500,
    )
    return {"requirements_text": (resp or "").strip(), "model_meta": meta}

def match_requirements_to_resume(resume_text: str, requirements_text: str) -> Dict[str, Any]:
    prompt = MATCH_REQUIREMENTS_PROMPT.format(
        requirements_text=requirements_text.strip(),
        resume_text=resume_text.strip(),
    )
    messages = [{"role": "user", "content": prompt}]
    resp, meta = ml_service.call_llm(
        messages=messages,
        model=MATCH_MODEL,
        call_type="match_requirements",
        max_tokens=1800,
    )
    return {"mapping_text": (resp or "").strip(), "model_meta": meta}

def research_company_via_web(company_name: Optional[str], company_url: Optional[str], min_results: int = 5) -> Dict[str, Any]:
    prompt = COMPANY_RESEARCH_PROMPT.format(
        company_name=(company_name or "").strip() or "(unknown)",
        company_url=(company_url or "").strip(),
    )
    resp = client.responses.create(
        model=WEB_MODEL,
        tools=[{"type": "web_search_preview"}],
        tool_choice={"type": "web_search_preview"},
        input=prompt,
        instructions=f"Use a web search tool and consult at least {min_results} credible results if needed.",
    )
    text = resp.output_text or ""
    evidence_links = []
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("http://") or s.startswith("https://"):
            evidence_links.append(s)
    return {"company_profile_text": text.strip(), "evidence_links": evidence_links[:5]}

def generate_tailored_resume_text(resume_text: str, mapping_text: str, company_profile_text: str) -> Dict[str, Any]:
    prompt = TAILOR_RESUME_PROMPT.format(
        resume_text=resume_text.strip(),
        mapping_text=mapping_text.strip(),
        company_profile_text=company_profile_text.strip(),
    )
    messages = [{"role": "user", "content": prompt}]
    resp, meta = ml_service.call_llm(
        messages=messages,
        model=RESUME_MODEL,
        call_type="tailor_resume",
        max_tokens=2400,
    )
    return {"tailored_resume_text": (resp or "").strip(), "model_meta": meta}

def generate_cover_letter_text(requirements_text: str, company_profile_text: str, about_me_or_prefs: str) -> Dict[str, Any]:
    prompt = COVER_LETTER_PROMPT.format(
        requirements_text=requirements_text.strip(),
        company_profile_text=company_profile_text.strip(),
        about_me_or_prefs=(about_me_or_prefs or "").strip(),
    )
    messages = [{"role": "user", "content": prompt}]
    resp, meta = ml_service.call_llm(
        messages=messages,
        model=COVER_LETTER_MODEL,
        call_type="cover_letter",
        max_tokens=900,
    )
    return {"cover_letter_text": (resp or "").strip(), "model_meta": meta}

# ---------- orchestrator ----------

def run_tailoring_pipeline(
    *,
    job_description: str,
    resume_pdf_bytes: Optional[bytes] = None,
    resume_text_fallback: Optional[str] = None,
    company_name: Optional[str] = None,
    company_url: Optional[str] = None,
    about_me_or_prefs: str = "",
    log_path: str = "runs_log.jsonl",
) -> Dict[str, Any]:

    # Step 1
    step1 = extract_requirements_from_jd(job_description)

    # Step 2 (resume parsing)
    if resume_pdf_bytes:
        resume_text = extract_text_from_pdf_bytes(resume_pdf_bytes)
    else:
        resume_text = (resume_text_fallback or "").strip()
    if not resume_text:
        raise ValueError("No resume text available (supply PDF bytes or fallback text).")

    # Step 3
    step2 = match_requirements_to_resume(resume_text, step1["requirements_text"])

    # Step 4
    step3 = research_company_via_web(company_name=company_name, company_url=company_url)

    # Step 5
    step4 = generate_tailored_resume_text(
        resume_text=resume_text,
        mapping_text=step2["mapping_text"],
        company_profile_text=step3["company_profile_text"],
    )

    # Step 6
    step5 = generate_cover_letter_text(
        requirements_text=step1["requirements_text"],
        company_profile_text=step3["company_profile_text"],
        about_me_or_prefs=about_me_or_prefs,
    )

    snapshot = {
        "timestamp": _now_iso(),
        "inputs": {
            "job_description": job_description,
            "company_name": company_name,
            "company_url": company_url,
            "about_me_or_prefs": about_me_or_prefs,
        },
        "resume_text_excerpt": resume_text[:4000],
        "requirements_text": step1["requirements_text"],
        "mapping_text": step2["mapping_text"],
        "company_profile_text": step3["company_profile_text"],
        "tailored_resume_text": step4["tailored_resume_text"],
        "cover_letter_text": step5["cover_letter_text"],
        "evidence_links": step3.get("evidence_links", []),
    }
    save_snapshot_jsonl(snapshot, path=log_path)

    return snapshot
