# AI Resume Analyzer

A Python-based web application that analyzes a resume against a job description and identifies matching and missing skills.

## Features
- Upload PDF and DOCX resumes
- Extract resume text
- Compare resume skills with job requirements
- Calculate skill match percentage
- Identify matched and missing skills
- Generate a downloadable PDF report

## Tech Stack
- Python
- Streamlit
- PyPDF2
- python-docx
- ReportLab

## Run Locally

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Start the application:

```bash
python3 -m streamlit run app.py
```

## Disclaimer
The match score is based on keyword-based skill matching and does not guarantee interview selection.