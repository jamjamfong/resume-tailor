# tailor.py — LLM tailoring logic

import os
import json
from dotenv import load_dotenv
load_dotenv()
from anthropic import Anthropic
from resume_data import (
    CONTACT, EDUCATION, WORK_EXPERIENCE,
    LEADERSHIP_EXPERIENCE, PROJECTS, SKILLS, HONORS
)

client = Anthropic()

SYSTEM_PROMPT = """You are an expert resume coach and ATS optimization specialist.
You will be given a job description and a candidate's full resume data.
Your job is to select and reframe the most relevant content for the role.

You must respond with ONLY valid JSON — no preamble, no markdown, no explanation.
You MUST include ALL fields exactly as specified.
No field may be omitted.
If a field has no value, use an empty string or empty list.
Failure to follow structure = invalid response.

Return this exact structure:
{
  "headline": "One-line personal summary tailored to the role (max 20 words)",
  "skills": {
    "category_name": ["skill1", "skill2", ...]
  },
  "work_experience": [
    {
      "title": "Job title (can be reframed slightly for relevance)",
      "company": "Company name",
      "location": "Location",
      "dates": "Dates",
      "bullets": ["bullet1", "bullet2", ...]
    }
  ],
  "leadership_experience": [
    {
      "title": "Role title",
      "org": "Org name",
      "location": "Location",
      "dates": "Dates",
      "bullets": ["bullet1", "bullet2", ...]
    }
  ],
  "projects": [
    {
      "name": "Project name",
      "bullets": ["bullet1", "bullet2", ...]
    }
  ],
  "coursework": ["Course 1", "Course 2", "Course 3", "Course 4", "Course 5"]
}

Rules:
- IMPORTANT: it MUST fit on one pdf page
- Rewrite bullets to use keywords and language from the job description
- Keep bullets achievement-oriented with metrics where possible
- Reorder skills categories to lead with what's most relevant to the role
- Select 2-4 bullets per role (prioritize impact and relevance)
- Include only projects relevant to the role; omit irrelevant ones
- Select 5 relevant courses from a typical CS/STS curriculum
- Keep all dates and company names accurate — do not fabricate
"""

def build_resume_context():
    """Serialize master resume into a readable string for the LLM."""
    lines = []

    lines.append("=== WORK EXPERIENCE ===")
    for job in WORK_EXPERIENCE:
        lines.append(f"{job['title']} | {job['company']} | {job['dates']}")
        for b in job['bullets']:
            lines.append(f"  - {b}")

    lines.append("\n=== LEADERSHIP EXPERIENCE ===")
    for role in LEADERSHIP_EXPERIENCE:
        lines.append(f"{role['title']} | {role['org']} | {role['dates']}")
        for b in role['bullets']:
            lines.append(f"  - {b}")

    lines.append("\n=== PROJECTS ===")
    for proj in PROJECTS:
        lines.append(f"{proj['name']}")
        for b in proj['bullets']:
            lines.append(f"  - {b}")

    lines.append("\n=== SKILLS ===")
    for category, items in SKILLS.items():
        lines.append(f"{category}: {', '.join(items)}")

    return "\n".join(lines)


def tailor_resume(job_description: str) -> dict:
    """Send JD + master resume to Claude, return tailored resume as dict."""

    resume_context = build_resume_context()

    user_message = f"""Here is the job description:
---
{job_description}
---

Here is my full resume:
---
{resume_context}
---

Please tailor my resume for this role and return the JSON structure.
"""

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}]
    )

    raw = response.content[0].text.strip()

    # Strip markdown fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    return json.loads(raw)


if __name__ == "__main__":
    # Quick test
    sample_jd = """
    We are looking for a Technical Program Manager to lead cross-functional AI initiatives.
    You will manage agile sprints, write PRDs, coordinate with engineering and product teams,
    and drive delivery of AI-powered features. Experience with JIRA, stakeholder management,
    and data-driven decision making required.
    """
    result = tailor_resume(sample_jd)
    print(json.dumps(result, indent=2))