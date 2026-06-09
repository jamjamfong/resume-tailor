# generate_pdf.py — ReportLab PDF builder

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from resume_data import CONTACT, EDUCATION, HONORS


# ── Styles ──────────────────────────────────────────────────────────────────

def make_styles():
    return {
        "name": ParagraphStyle(
            "name",
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=19,
            alignment=TA_CENTER,
            spaceAfter=2,
        ),
        "contact": ParagraphStyle(
            "contact",
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            alignment=TA_CENTER,
            spaceAfter=6,
        ),
        "section_header": ParagraphStyle(
            "section_header",
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=13,
            spaceBefore=6,
            spaceAfter=2,
            textTransform="uppercase",
        ),
        "job_title": ParagraphStyle(
            "job_title",
            fontName="Helvetica-Bold",
            fontSize=9.5,
            leading=12,
        ),
        "job_meta": ParagraphStyle(
            "job_meta",
            fontName="Helvetica-Oblique",
            fontSize=9,
            leading=11,
            spaceAfter=2,
        ),
        "bullet": ParagraphStyle(
            "bullet",
            fontName="Helvetica",
            fontSize=9,
            leading=11.5,
            leftIndent=14,
            bulletIndent=4,
            spaceAfter=2.5,
        ),
        "skills_label": ParagraphStyle(
            "skills_label",
            fontName="Helvetica-Bold",
            fontSize=9,
            leading=12,
        ),
        "skills_value": ParagraphStyle(
            "skills_value",
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            spaceAfter=2,
        ),
        "edu": ParagraphStyle(
            "edu",
            fontName="Helvetica",
            fontSize=9,
            leading=12,
        ),
        "honors": ParagraphStyle(
            "honors",
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            spaceAfter=2,
        ),
    }


# ── Helpers ──────────────────────────────────────────────────────────────────

def section_divider(story, s, label):
    story.append(Spacer(1, 4))
    story.append(Paragraph(label, s["section_header"]))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.black, spaceAfter=3))


def date_row(left_text, right_text, left_style, right_style, col_widths=(4.5*inch, 2.0*inch)):
    """Two-column row: left-aligned title, right-aligned date."""
    t = Table(
        [[Paragraph(left_text, left_style), Paragraph(right_text, right_style)]],
        colWidths=col_widths,
    )
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return t


# ── Section builders ─────────────────────────────────────────────────────────

def add_header(story, s):
    story.append(Paragraph(CONTACT["name"], s["name"]))
    contact_line = f"{CONTACT['phone']}  |  {CONTACT['email']}  |  {CONTACT['linkedin']}  |  {CONTACT['github']}"
    story.append(Paragraph(contact_line, s["contact"]))


def add_education(story, s, coursework=None):
    section_divider(story, s, "Education")
    for edu in EDUCATION:
        degrees = " & ".join(edu["degrees"])
        story.append(date_row(
            f"<b>{edu['school']}</b>",
            edu["dates"],
            s["job_title"],
            ParagraphStyle("right", fontName="Helvetica", fontSize=9, alignment=TA_RIGHT),
        ))
        story.append(Paragraph(f"{degrees} | Minor: {edu['minor']}", s["edu"]))
        if coursework:
            story.append(Paragraph(f"<i>Relevant Coursework:</i> {', '.join(coursework)}", s["edu"]))
        story.append(Spacer(1, 3))


def add_experience_section(story, s, label, entries):
    section_divider(story, s, label)
    right_style = ParagraphStyle("right", fontName="Helvetica", fontSize=9, alignment=TA_RIGHT)
    for entry in entries:
        title = entry.get("title", "")
        org = entry.get("company") or entry.get("org", "")
        location = entry.get("location", "")
        dates = entry.get("dates", "")

        story.append(date_row(
            f"<b>{title}</b>  |  {org}  |  {location}",
            dates,
            s["job_title"],
            right_style,
        ))
        for bullet in entry.get("bullets", []):
            story.append(Paragraph(f"• {bullet}", s["bullet"]))
        story.append(Spacer(1, 3))


def add_projects(story, s, projects):
    section_divider(story, s, "Projects")
    for proj in projects:
        story.append(Paragraph(f"<b>{proj['name']}</b>", s["job_title"]))
        for bullet in proj.get("bullets", []):
            story.append(Paragraph(f"• {bullet}", s["bullet"]))
        story.append(Spacer(1, 3))


def add_skills(story, s, skills):
    section_divider(story, s, "Skills")
    for category, items in skills.items():
        line = f"<b>{category}:</b>  {', '.join(items)}"
        story.append(Paragraph(line, s["skills_value"]))


def add_honors(story, s):
    section_divider(story, s, "Honors / Awards")
    right_style = ParagraphStyle("right", fontName="Helvetica", fontSize=9, alignment=TA_RIGHT)
    for h in HONORS:
        story.append(date_row(
            f"<b>{h['title']}</b>  |  {h['org']}  |  {h['location']}",
            h["date"],
            s["honors"],
            right_style,
        ))


# ── Main generator ───────────────────────────────────────────────────────────

def generate_pdf(tailored: dict, output_path: str):
    """
    Takes the tailored dict from tailor.py and writes a PDF to output_path.
    """
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=0.65 * inch,
        rightMargin=0.65 * inch,
        topMargin=0.55 * inch,
        bottomMargin=0.55 * inch,
    )

    s = make_styles()
    story = []

    add_header(story, s)

    add_education(story, s, coursework=tailored.get("coursework"))

    if tailored.get("work_experience"):
        add_experience_section(story, s, "Work Experience", tailored["work_experience"])

    if tailored.get("leadership_experience"):
        add_experience_section(story, s, "Leadership Experience", tailored["leadership_experience"])

    if tailored.get("projects"):
        add_projects(story, s, tailored["projects"])

    if tailored.get("skills"):
        add_skills(story, s, tailored["skills"])

    add_honors(story, s)

    doc.build(story)
    print(f"PDF saved to {output_path}")


if __name__ == "__main__":
    # Test with dummy data
    dummy = {
        "coursework": ["Machine Learning", "Software Engineering", "Data Structures", "AI Ethics", "Database Systems"],
        "work_experience": [
            {
                "title": "AI PM and Business Operations Intern",
                "company": "HELO Solutions",
                "location": "Remote",
                "dates": "Aug 2025 – Oct 2025",
                "bullets": [
                    "Led Agile product operations for 3 active AI product lines",
                    "Automated meeting documentation using prompt engineering, saving 10+ hours/week",
                ]
            }
        ],
        "leadership_experience": [],
        "projects": [],
        "skills": {
            "Tools": ["JIRA", "Linear", "Figma", "Git"],
            "Languages": ["Python", "SQL", "JavaScript"],
        },
    }
    generate_pdf(dummy, "/tmp/test_resume.pdf")