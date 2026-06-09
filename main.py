# main.py — CLI entrypoint

import argparse
import os
import sys
from dotenv import load_dotenv

load_dotenv()

from tailor import tailor_resume
from generate_pdf import generate_pdf


def main():
    parser = argparse.ArgumentParser(
        description="AI-powered resume tailor — generates a role-specific PDF from a job description."
    )
    parser.add_argument(
        "--jd",
        type=str,
        help="Path to a .txt file containing the job description",
    )
    parser.add_argument(
        "--jd-text",
        type=str,
        help="Job description as a direct string (use quotes)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="resume_tailored.pdf",
        help="Output PDF filename (default: resume_tailored.pdf)",
    )

    args = parser.parse_args()

    # ── Get job description ───────────────────────────────────────────────
    if args.jd:
        if not os.path.exists(args.jd):
            print(f"Error: file not found: {args.jd}")
            sys.exit(1)
        with open(args.jd, "r") as f:
            job_description = f.read()
    elif args.jd_text:
        job_description = args.jd_text
    else:
        # Interactive mode — paste JD in terminal
        print("Paste the job description below. When done, enter a blank line followed by END:")
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        job_description = "\n".join(lines)

    if not job_description.strip():
        print("Error: job description is empty.")
        sys.exit(1)

    # ── Tailor ────────────────────────────────────────────────────────────
    print("Tailoring resume with Claude...")
    try:
        tailored = tailor_resume(job_description)
    except Exception as e:
        print(f"Error during tailoring: {e}")
        sys.exit(1)

    # ── Generate PDF ──────────────────────────────────────────────────────
    print("Generating PDF...")
    try:
        generate_pdf(tailored, args.output)
    except Exception as e:
        print(f"Error during PDF generation: {e}")
        sys.exit(1)

    print(f"\nDone! Resume saved to: {args.output}")


if __name__ == "__main__":
    main()