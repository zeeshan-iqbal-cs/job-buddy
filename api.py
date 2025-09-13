# api.py
from fastapi import FastAPI, UploadFile, File, Form, Query, Body
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from typing import Optional, List, Dict, Any
import json

from main import run_tailoring_pipeline

app = FastAPI(title="Job Buddy API", version="0.6.0", docs_url="/api/docs", redoc_url="/api/redoc")

HISTORY_PATH = Path(__file__).parent / "runs_log.jsonl"

# ---------- utils ----------
def _read_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    out: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except Exception:
                continue
    return out

def _write_jsonl(path: Path, items: List[Dict[str, Any]]) -> None:
    tmp = path.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")
    tmp.replace(path)

def _tracking_defaults(tr: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    tr = tr or {}
    return {
        "applied": bool(tr.get("applied", False)),
        "platform": tr.get("platform", ""),
        "application_url": tr.get("application_url", ""),
        "status": tr.get("status", "Draft"),
        "notes": tr.get("notes", ""),
    }

# ---------- api ----------
@app.get("/api/health")
def health():
    from datetime import datetime, timezone
    return {"status": "ok", "time": datetime.now(tz=timezone.utc).isoformat()}

@app.post("/api/generate")
async def generate(
    resume_file: UploadFile = File(...),
    job_description: str = Form(...),
    company_url: Optional[str] = Form(None),
    about_me: Optional[str] = Form(None),
):
    try:
        resume_bytes = await resume_file.read()
        results = run_tailoring_pipeline(
            job_description=job_description,
            resume_pdf_bytes=resume_bytes,
            resume_text_fallback=None,
            company_name=None,
            company_url=company_url,
            about_me_or_prefs=about_me or "",
            log_path=str(HISTORY_PATH),
        )
        return JSONResponse(status_code=200, content={
            "timestamp": results.get("timestamp"),
            "requirements_text": results.get("requirements_text", ""),
            "mapping_text": results.get("mapping_text", ""),
            "company_profile_text": results.get("company_profile_text", ""),
            "evidence_links": results.get("evidence_links", []),
            "tailored_resume_text": results.get("tailored_resume_text", ""),
            "cover_letter_text": results.get("cover_letter_text", ""),
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"generation_failed: {e}"})

@app.get("/api/history")
def history(limit: int = Query(50, ge=1, le=500), offset: int = Query(0, ge=0)):
    """
    Newest-first summary for table, including the big text fields the user
    asked for (so the UI can render them as Markdown directly in cells).
    """
    items = list(reversed(_read_jsonl(HISTORY_PATH)))  # newest first
    slice_ = items[offset: offset + limit]
    summarized: List[Dict[str, Any]] = []
    for i, it in enumerate(slice_):
        inputs = it.get("inputs", {}) or {}
        extracted = it.get("extracted", {}) or {}
        outputs = it.get("outputs", {}) or {}
        tr = _tracking_defaults(it.get("tracking"))

        summarized.append({
            "idx": offset + i,  # newest-first index
            "timestamp": it.get("timestamp"),
            "company_name": inputs.get("company_name") or inputs.get("company_url") or "",

            # requested columns (full text so we can render as markdown)
            "job_description": inputs.get("job_description", ""),
            "about_me_or_prefs": inputs.get("about_me_or_prefs", ""),
            "resume_text_excerpt": extracted.get("resume_text_excerpt", ""),
            "mapping_text": it.get("mapping") or it.get("mapping_text", ""),
            "tailored_resume_text": outputs.get("tailored_resume_text", ""),
            "cover_letter_text": outputs.get("cover_letter_text", ""),

            # evidence
            "evidence_links": it.get("evidence_links", []),

            # tracking / editable
            "applied": tr["applied"],
            "platform": tr["platform"],
            "application_url": tr["application_url"],
            "status": tr["status"],
            "notes": tr["notes"],
        })
    return {"items": summarized, "total": len(items)}

@app.get("/api/history/detail")
def history_detail(index: int = Query(..., ge=0)):
    items = list(reversed(_read_jsonl(HISTORY_PATH)))  # newest first
    print(items[0].keys())
    if index >= len(items):
        return JSONResponse(status_code=404, content={"error": "index out of range"})
    return items[index]

@app.post("/api/history/update")
def history_update(payload: Dict[str, Any] = Body(...)):
    try:
        index = int(payload.get("index"))
    except Exception:
        return JSONResponse(status_code=400, content={"error": "invalid index"})

    items_oldest = _read_jsonl(HISTORY_PATH)             # oldest first
    items_newest = list(reversed(items_oldest))          # newest first
    if index < 0 or index >= len(items_newest):
        return JSONResponse(status_code=404, content={"error": "index out of range"})

    run_obj = items_newest[index]
    tr = _tracking_defaults(run_obj.get("tracking"))
    for key in ("applied", "platform", "application_url", "status", "notes"):
        if key in payload and payload[key] is not None:
            tr[key] = payload[key]
    run_obj["tracking"] = tr

    items_newest[index] = run_obj
    _write_jsonl(HISTORY_PATH, list(reversed(items_newest)))  # write back oldest first
    return {"ok": True, "tracking": tr}

# ---------- static ----------
static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True)

@app.get("/", include_in_schema=False)
def serve_index():
    return FileResponse(static_dir / "index.html")

app.mount("/static", StaticFiles(directory=static_dir), name="static")
