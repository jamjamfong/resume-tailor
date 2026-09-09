# app.py — lightweight web UI for the AI Resume Tailor Tool

import os
import tempfile
import uuid

from flask import Flask, render_template, request, send_file, flash, redirect, url_for

from tailor import tailor_resume
from generate_pdf import generate_pdf

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-change-me")

# Temp directory for generated PDFs (cleared per run, not persisted)
OUTPUT_DIR = os.path.join(tempfile.gettempdir(), "resume_tailor_outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/tailor", methods=["POST"])
def tailor():
    job_description = request.form.get("job_description", "").strip()

    if not job_description:
        flash("Please paste a job description before submitting.")
        return redirect(url_for("index"))

    try:
        tailored = tailor_resume(job_description)
    except Exception as e:
        flash(f"Something went wrong while tailoring your resume: {e}")
        return redirect(url_for("index"))

    output_filename = f"resume_{uuid.uuid4().hex[:8]}.pdf"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    try:
        generate_pdf(tailored, output_path)
    except Exception as e:
        flash(f"Something went wrong while generating the PDF: {e}")
        return redirect(url_for("index"))

    return send_file(
        output_path,
        as_attachment=True,
        download_name="tailored_resume.pdf",
        mimetype="application/pdf",
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)