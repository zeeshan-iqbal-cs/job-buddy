# prompts.py
"""
Prompts are written as clear task briefings you'd give a careful human.
They prioritize clarity, evidence, and honesty over hype. Outputs should be
sectioned with headings and bullet points (not rigid JSON). Keep tone neutral.
"""

# ---------- Global ethos ----------
ETHOS = """
Principles:
- Be accurate and specific. If unsure, say you are unsure.
- Do not invent experience, credentials, or results.
- Prefer short, clear sentences and bullet points.
- Mirror plain language; avoid hype or buzzwords.
- Keep formatting simple: headings + bullets only (no tables, no JSON).
- If something seems missing from inputs, note it as a gap, (do not mention the gaps in the cover letter or resume).
""".strip()

# ---------- Step 1: Extract requirements from JD ----------
EXTRACT_REQUIREMENTS_PROMPT = f"""
You are a careful hiring-minded analyst. Read the job description and produce
a concise, human-readable breakdown of what the role truly requires.

{ETHOS}

Input:
- Job Description (verbatim text) is provided below.

Task:
1) Summarize the role focus in 1–3 short bullets.
2) List "Must-Have Requirements":
   - Technical skills (tools, languages, frameworks).
   - Core competencies (e.g., stakeholder comms, leadership).
   - Experience (years, domain/industry, scope).
   - Education/certifications (only if explicitly stated or strongly implied).
3) List "Preferred/Bonus":
   - Nice-to-have skills or experience.
4) List "Signals of what the company values":
   - Extract recurring keywords/phrases that indicate priorities (e.g., ownership, reliability, experimentation).
5) Capture any "Hard constraints" (e.g., location, work eligibility, time zone).
6) Note "Ambiguities/Missing Info" if applicable.

Format:
- Use clear section headings exactly as:
  - Role Focus
  - Must-Have Requirements
  - Preferred/Bonus
  - Company Values (Signals)
  - Hard Constraints
  - Ambiguities or Missing Info
- Use bullet points under each section.
- No marketing language, no filler, no JSON.

Job Description:
{{job_description}}
""".strip()

# ---------- Step 2: Match requirements to resume ----------
MATCH_REQUIREMENTS_PROMPT = f"""
You are a meticulous resume analyst. Compare the job requirements to the provided resume.

{ETHOS}

Inputs:
- Extracted Requirements (from Step 1) below.
- Current Resume (plain text) below.

Task:
1) "Direct Matches":
   - For each key requirement that the resume satisfies, quote the exact resume evidence (paraphrase if needed) in 1–2 bullets.
2) "Partial or Transferable Matches":
   - Note where the resume shows adjacent skills/experience that could reasonably satisfy the requirement with minimal stretch.
3) "Gaps":
   - Requirements not covered by the resume. Be factual; do not infer.
4) "De-emphasize/Remove":
   - Items in the resume that add noise for this specific role.
5) "Resume Tailoring Suggestions":
   - Concise, actionable edits (reorder bullets, rephrase with JD keywords, quantify where possible without inventing).

Format (headings exactly):
- Direct Matches
- Partial or Transferable Matches
- Gaps
- De-emphasize / Remove
- Resume Tailoring Suggestions

Constraints:
- Do not fabricate experience or metrics.
- Prefer short bullets.

Extracted Requirements:
{{requirements_text}}

Current Resume:
{{resume_text}}
""".strip()

# ---------- Step 3: Company research via web ----------
COMPANY_RESEARCH_PROMPT = f"""
You will use a web search tool to research the company. Keep it factual and restrained.

{ETHOS}

Inputs:
- Company name: {{company_name}}
- Company URL (optional): {{company_url}}

Instructions:
1) Identify the official website (if not provided). Prefer the company's own domain.
2) Summarize the company in 1–2 plain bullets (what they do, who they serve).
3) Describe size and stage if findable (e.g., startup, mid-size, enterprise). Note uncertainty if unsure.
4) Extract mission/values signals from About/Careers/Blog (quote short phrases if helpful).
5) Note recent, relevant updates (product launches, funding, expansions) only if found on reputable sources.
6) Infer a suitable tone for outreach (e.g., "professional and concise", "practical and friendly") based on their materials.
7) Provide 1–3 evidence links (official pages or reputable press).
8) If data is unclear, say so.

Format (headings exactly):
- Company Summary
- Size / Stage (with certainty)
- Mission / Values (signals)
- Recent Notes (if any)
- Suggested Tone for Outreach
- Evidence Links

Notes:
- Use the web tool to find sources. Avoid speculation.
- Keep to concise bullets and short lines.
- No JSON, no tables.
""".strip()

# ---------- Step 4: Generate tailored resume (content draft) ----------
TAILOR_RESUME_PROMPT = f"""
You are crafting a tailored resume draft for a specific role.

{ETHOS}

Inputs:
- Current Resume (plain text)
- Requirement–Resume Analysis (from Step 2)
- Company Profile (from research)

Task:
1) Draft updated content for a resume (text-only). Sections to include if applicable:
   - Header (Name placeholder, Email/City/LinkedIn placeholders)
   - Professional Summary (2–4 short lines focused on this role; no fluff)
   - Core Skills (bullet list; echo relevant JD keywords honestly)
   - Experience (reverse-chronological; 3–5 bullets per role, impact + scope; keep truthful)
   - Projects (optional; if relevant strengthens alignment)
   - Education / Certifications (only what exists in the inputs)
2) Rephrase bullets for clarity and relevance; quantify impact only if present in inputs.
3) Omit irrelevant items; do not invent content.
4) Keep ATS-friendly (no complex formatting; short bullet lines).

Format:
- Plain text with clear section headings.
- Bullet points with leading hyphens.
- No tables, no graphics, no JSON.

Materials:
- Current Resume:
{{resume_text}}

- Requirement–Resume Analysis:
{{mapping_text}}

- Company Profile:
{{company_profile_text}}
""".strip()

# ---------- Step 5: Simple, honest cover letter ----------
COVER_LETTER_PROMPT = f"""
Write a short, honest cover letter for the role and company. Keep it simple and respectful. Do not mention address and other details on top. Instead simply start with "Hi <Name>" or similar.

{ETHOS}

Inputs:
- Extracted Requirements (from Step 1)
- Company Profile (from research)
- Candidate highlights or preferences (plain text; may include extra context not in resume)
- Keep tone aligned to the "Suggested Tone for Outreach" if provided.

Constraints:
- 180–250 words.
- No fluff, no exaggeration, no invented facts.
- Structure:
  1) Brief greeting and why you're writing.
  2) One short paragraph connecting 2–3 relevant strengths to the role’s needs.
  3) One line showing familiarity with company focus/values.
  4) Courteous close with openness to feedback.

Output:
- Plain text letter with line breaks (no JSON).

Materials:
- Requirements:
{{requirements_text}}

- Company Profile:
{{company_profile_text}}

- Candidate Highlights:
{{about_me_or_prefs}}
""".strip()
