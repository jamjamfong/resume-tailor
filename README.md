# AI Resume Tailor

A project born from my frustration with having to tailor my resume for every job that I applied to.

Given a job description, it uses Claude to rewrite and reprioritize your resume content for that specific role, then generates a clean, one-page PDF. Available two ways: from the command line, or through a simple local web page.

## Setup

1. Clone the repo and move into it:
   ```
   git clone <your-repo-url>
   cd resume-tailor
   ```

2. Create and activate a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate       # Windows: venv\Scripts\activate
   ```
   You'll need to run the `source` command again each time you open a new terminal window — activation doesn't persist across sessions.

3. Install dependencies:
   ```
   pip install -r requirements.txt
   pip install flask python-dotenv
   ```

4. Add your Anthropic API key. Create a file named `.env` in the project root:
   ```
   ANTHROPIC_API_KEY=your-key-here
   ```

## Usage

### Web UI (recommended)

```
python3 app.py
```

Then open `http://localhost:5000` in your browser, paste a job description into the textarea, and click "Tailor my resume." A tailored PDF downloads automatically after a few seconds.

### Command line

Paste a job description into a `.txt` file, then run:
```
python3 main.py --jd job_description.txt --output resume_output.pdf
```

Or pass the job description directly as a string:
```
python3 main.py --jd-text "paste the job description here" --output resume_output.pdf
```

Or run it with no arguments for interactive mode, and paste the job description directly into the terminal when prompted.

## How it works

- `resume_data.py` holds your full master resume — every job, project, and skill you might ever want to include.
- `tailor.py` sends the job description plus your full resume to Claude, which selects and rewrites the most relevant content for that specific role.
- `generate_pdf.py` takes Claude's tailored output and lays it out as a one-page PDF using ReportLab.
- `main.py` is the command-line entrypoint; `app.py` is the web UI entrypoint. Both call the same underlying `tailor.py` and `generate_pdf.py` — there's no duplicated logic between the two.

## Project structure

```
resume-tailor/
├── .env                 # your API key (not committed)
├── requirements.txt
├── resume_data.py        # master resume content
├── tailor.py              # Claude tailoring logic
├── generate_pdf.py        # PDF generation
├── main.py                # CLI entrypoint
├── app.py                 # web UI entrypoint
└── templates/
    └── index.html         # web UI form page
```

## Notes

- Never commit your `.env` file — it contains your live API key.
- All dates, company names, and factual details in `resume_data.py` are kept accurate; Claude is only instructed to reframe and prioritize, not fabricate.