"""Core mentoring workflow for Campus Research Mentor."""


def build_prompt(profile: dict[str, str]) -> str:
    """Build the grounded mentoring request from a learner profile."""
    return f"""
Student profile:
- Name: {profile['student_name']}
- Program level: {profile['program_level']}
- Year/Semester: {profile['year_semester']}
- Areas of interest: {profile['interests']}
- Current skills: {profile['skills']}
- Preferred project type: {profile['project_type']}
- Compute available: {profile['compute']}
- Desired difficulty: {profile['difficulty']}
- Time available: {profile['timeline']}
- Local/community relevance wanted: {profile['local_relevance']}
- Extra notes: {profile['notes']}

Task:
Generate exactly 3 project ideas. Make them distinct.
For each idea include:
1. Title
2. Why this fits the student
3. Problem statement
4. Minimum viable implementation
5. Stretch goal
6. Dataset / benchmark / source of evaluation
7. Tools / languages / frameworks
8. Risks or common mistakes
9. A 4-week starter plan

End with a short recommendation on which idea should be started first.
""".strip()


def fallback_response() -> str:
    """Return an explicitly labelled offline demonstration response."""
    return """
## Idea 1: Secure Lab Assistant for Programming Courses
**Why this fits:** Matches systems security and software engineering interests while staying feasible on laptop-only compute.

## Idea 2: Campus Research Mentor for Topic Scoping
**Why this fits:** Directly aligned with mentoring bottlenecks in large CS classrooms.

## Idea 3: Lightweight Threat Modeling Assistant for Student Projects
**Why this fits:** Strong match for systems security interest and final-year project needs.

### Recommended starting point
Start with **Idea 2** because it is highly feasible and easy to demonstrate clearly.
""".strip()


def call_vertex_ai(user_prompt, project_id, location, model_name, client_factory=None):
    """Call Gemini through Vertex AI using server-side application credentials."""
    if client_factory is None:
        from google import genai
        client_factory = genai.Client
    client = client_factory(vertexai=True, project=project_id, location=location)
    response = client.models.generate_content(model=model_name, contents=user_prompt)
    return response.text
