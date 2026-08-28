# Campus Research Mentor Demo

A minimal Streamlit app for the **Campus Research Mentor** project.

## What it does
This app collects a student profile and generates structured project ideas. It supports:
- Demo mode with built-in sample output
- Live mode using **Gemini on Vertex AI**

## Files
- `app.py` — Streamlit application
- `requirements.txt` — Python dependencies
- `README.md` — run and deploy instructions

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Authenticate for Vertex AI
Google Cloud documents that Gemini on Vertex AI can be accessed using Application Default Credentials, and recommends `gcloud auth application-default login` for local authentication.

```bash
gcloud auth application-default login
```

Set your project and location as environment variables if desired:
```bash
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_LOCATION="us-central1"
export GEMINI_MODEL="gemini-2.5-flash"
```

## Deploy to Cloud Run
Google Cloud's Streamlit on Cloud Run quickstart shows deployment from source with a public service URL.

```bash
gcloud run deploy campus-research-mentor   --source .   --region us-central1   --allow-unauthenticated
```

After deployment, Cloud Run returns a service URL that can be used as the live project link.

## Notes
- The app defaults to built-in demo output so it still works without credentials.
- For your Gen AI Academy APAC submission, use the deployed Cloud Run URL as the demo link.
