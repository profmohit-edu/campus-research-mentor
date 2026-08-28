# Campus Research Mentor

**Gemini-Powered AI Research Mentoring Assistant**

Campus Research Mentor is a Streamlit working model created by **Mohit Tiwari**, Assistant Professor, Department of Computer Science and Engineering, Bharati Vidyapeeth's College of Engineering, New Delhi.

## Live working model

https://campus-research-mentor-89358699376.us-central1.run.app/

The application converts a student or early-researcher profile into three distinct, feasible project directions. Each direction contains a problem statement, profile-fit explanation, minimum viable implementation, stretch goal, evaluation source, tools, risks, four-week starter plan, and final recommendation.

## Executed workflow

1. The learner supplies programme level, semester, interests, skills, project type, compute availability, difficulty, timeline, relevance requirement, and notes.
2. `mentor.build_prompt` converts that context into a bounded mentoring request.
3. `mentor.call_vertex_ai` invokes Gemini through the Vertex AI client.
4. The UI identifies successful production output as **Vertex AI / Gemini**.
5. Provider failure is displayed as an error and any fallback is separately identified as demonstration output.

## Architecture and security

```text
Streamlit profile form
        -> structured mentoring prompt
        -> google.genai Vertex AI client
        -> Gemini model
        -> structured project/research guidance
```

Production uses `google.genai.Client(vertexai=True, project=..., location=...)`. Cloud Run supplies server-side Application Default Credentials through the service identity. No Gemini API key or service-account private key is stored in the repository or sent to browser JavaScript.

Configuration is supplied through environment variables: `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION`, and `GEMINI_MODEL`.

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Authenticate for Vertex AI

Use Application Default Credentials for local development:

```bash
gcloud auth application-default login
```

Set your project and location as environment variables if desired:
```bash
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_LOCATION="us-central1"
export GEMINI_MODEL="gemini-2.5-flash"
```

## Tests

The tests verify learner-context prompt construction, required output structure, the Vertex AI configuration boundary, response handling, and provider-failure propagation.

```bash
python -m compileall -q app.py mentor.py tests
python -m unittest discover -s tests -v
```

## Deploy to Cloud Run

```bash
gcloud run deploy campus-research-mentor \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_CLOUD_PROJECT=your-project-id,GOOGLE_CLOUD_LOCATION=us-central1,GEMINI_MODEL=gemini-2.5-flash
```

Grant the Cloud Run service identity the minimum Vertex AI permissions required by the selected model. Never place credentials in source files or frontend configuration.

## Provenance

The original implementation was committed by Mohit Tiwari on 29 May 2026 as `Initial release: Campus Research Mentor`. Repository publication and test/documentation strengthening use truthful current commit dates; no history is backdated.
