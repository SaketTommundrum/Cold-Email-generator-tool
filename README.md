# Cold Email Generator Tool

Generate tailored outreach content from job posting URLs using Groq + LangChain.

## Features

- Extracts job details from a job URL
- Generates a personalized cold email
- Generates a LinkedIn outreach post
- Optional hiring manager LinkedIn URL input for personalization

## Local setup

1. Create and activate a virtual environment
2. Install dependencies
3. Add environment variables in `app/.env`
4. Run Streamlit app

## Environment variables

Create `app/.env` with:

```env
GROQ_API_KEY=your_groq_api_key_here
USER_AGENT=ColdEmailGenerator/1.0
```

## Run

From the project root:

```powershell
& ".\.venv\Scripts\python.exe" -m streamlit run .\app\main.py
```

## Before publishing to GitHub

- Ensure `.gitignore` is present (already added)
- Remove any previously tracked secrets/data:

```powershell
git rm --cached app/.env
git rm -r --cached vectorstore
```

- If a real API key was ever committed, rotate/revoke it in your provider dashboard.
- <img width="1836" height="769" alt="Screenshot 2026-03-04 082259" src="https://github.com/user-attachments/assets/e5e4904c-b802-4074-a5e5-78b1f074fbcb" />

