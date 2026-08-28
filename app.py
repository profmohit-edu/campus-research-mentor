import os
import streamlit as st

st.set_page_config(page_title="Campus Research Mentor", page_icon="🎓", layout="wide")

st.title("Campus Research Mentor")

st.markdown(
    """
**A Gemini-powered assistant for guiding CS students from interest to implementable research projects.**

**Builder**  
Mohit Tiwari  
Assistant Professor, Department of Computer Science and Engineering  
Bharati Vidyapeeth's College of Engineering (BVCOE, Delhi)
""".strip()
)

with st.sidebar:
    st.header("Configuration")
    use_live = st.toggle("Use live Vertex AI / Gemini", value=True)
    project_id = st.text_input("Google Cloud Project ID", value=os.getenv("GOOGLE_CLOUD_PROJECT", "mohit-mentor-ai"))
    location = st.text_input("Vertex AI location", value=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"))
    model_name = st.text_input("Model name", value=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"))

    st.markdown("---")
    st.subheader("Builder profile")
    st.markdown(
        """
**Mohit Tiwari**  
Assistant Professor, Department of Computer Science and Engineering  
Bharati Vidyapeeth's College of Engineering (BVCOE, Delhi)

Campus Research Mentor is a Gen AI academic mentoring assistant designed to help CS students move from broad interests to feasible project and early research directions, especially in large classroom settings.
""".strip()
    )

    st.markdown(
        """
**Project links**  
• Live demo: https://campus-research-mentor-89358699376.us-central1.run.app/  
• GitHub: https://github.com/profmohit-edu/campus-research-mentor
""".strip()
    )

    with st.expander("Academic profiles"):
        st.markdown(
            """
- ORCID: https://orcid.org/0000-0003-1836-3451  
- Google Scholar: https://scholar.google.com/citations?user=ZFRPBBcAAAAJ&hl=en  
- Scopus: https://www.scopus.com/authid/detail.uri?authorId=24483852000  
- Web of Science: https://www.webofscience.com/wos/author/record/33087873  
- Vidwan: https://vidwan.inflibnet.ac.in/profile/293249  
- ResearchGate: https://www.researchgate.net/profile/Mohit-Tiwari-6  
- LinkedIn: https://www.linkedin.com/in/mtiw
""".strip()
        )

col1, col2 = st.columns([1, 1])

with col1:
    student_name = st.text_input("Student name", value="Aarav")
    program_level = st.selectbox("Program level", ["B.Tech", "M.Tech", "PhD coursework", "Self-led learner"], index=0)
    year_semester = st.text_input("Year / Semester", value="3rd year, Semester 6")
    interests = st.text_area("Areas of interest", value="Systems security, machine learning, software engineering")
    skills = st.text_area("Current skills", value="Python, C++, data structures, OS basics, beginner ML")
    project_type = st.selectbox("Preferred project type", ["Course project", "Final year project", "Research exploration", "Hackathon prototype"], index=1)

with col2:
    compute = st.selectbox("Available compute", ["Laptop only", "Laptop + free cloud credits", "GPU lab access", "Unclear / limited"], index=0)
    difficulty = st.selectbox("Desired difficulty", ["Beginner", "Intermediate", "Advanced"], index=1)
    timeline = st.selectbox("Time available", ["4 weeks", "8 weeks", "1 semester", "2 semesters"], index=2)
    local_relevance = st.selectbox("Need local/community relevance?", ["Yes", "No", "Optional"], index=2)
    notes = st.text_area("Extra notes", value="Should be feasible for a student team of 2 and suitable for faculty review.")

prompt = f"""
Student profile:
- Name: {student_name}
- Program level: {program_level}
- Year/Semester: {year_semester}
- Areas of interest: {interests}
- Current skills: {skills}
- Preferred project type: {project_type}
- Compute available: {compute}
- Desired difficulty: {difficulty}
- Time available: {timeline}
- Local/community relevance wanted: {local_relevance}
- Extra notes: {notes}

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

def fallback_response():
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

def call_vertex_ai(user_prompt: str, project_id: str, location: str, model_name: str) -> str:
    from google import genai
    client = genai.Client(vertexai=True, project=project_id, location=location)
    response = client.models.generate_content(
        model=model_name,
        contents=user_prompt,
    )
    return response.text

if st.button("Generate project ideas", type="primary", use_container_width=True):
    try:
        if use_live and project_id:
            answer = call_vertex_ai(prompt, project_id, location, model_name)
            st.markdown("**Mode:** Vertex AI / Gemini")
        else:
            answer = fallback_response()
            st.markdown("**Mode:** Built-in demo output")
        st.markdown(answer)
    except Exception as e:
        st.error(f"Live call failed: {e}")
        st.info("Showing fallback demo response instead.")
        st.markdown(fallback_response())

with st.expander("Why this helps"):
    st.markdown(
        """
- Reduces project-scoping friction for students.
- Gives faculty a structured first draft to refine.
- Produces consistent outputs for large classrooms.
- Can later be grounded with lab notes, faculty guidelines, or prior project abstracts.
""".strip()
    )