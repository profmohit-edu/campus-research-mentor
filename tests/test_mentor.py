import unittest
from mentor import build_prompt, call_vertex_ai, fallback_response

PROFILE = {
    "student_name": "Demo Student", "program_level": "B.Tech",
    "year_semester": "3rd year, Semester 6",
    "interests": "systems security and machine learning",
    "skills": "Python and operating-system basics",
    "project_type": "Final year project", "compute": "Laptop only",
    "difficulty": "Intermediate", "timeline": "1 semester",
    "local_relevance": "Optional", "notes": "Team of two",
}

class PromptTests(unittest.TestCase):
    def test_profile_context_is_included(self):
        prompt = build_prompt(PROFILE)
        self.assertIn("systems security and machine learning", prompt)
        self.assertIn("Laptop only", prompt)
        self.assertIn("Team of two", prompt)

    def test_required_mentoring_structure_is_requested(self):
        prompt = build_prompt(PROFILE)
        self.assertIn("Generate exactly 3 project ideas", prompt)
        self.assertIn("Minimum viable implementation", prompt)
        self.assertIn("A 4-week starter plan", prompt)
        self.assertIn("recommendation", prompt)

    def test_fallback_is_bounded_and_explicit(self):
        response = fallback_response()
        self.assertIn("Idea 1", response)
        self.assertIn("Recommended starting point", response)

class VertexBoundaryTests(unittest.TestCase):
    def test_vertex_configuration_and_prompt_are_forwarded(self):
        calls = {}
        class Models:
            def generate_content(self, **kwargs):
                calls["generate"] = kwargs
                return type("Response", (), {"text": "grounded mentoring output"})()
        class Client:
            def __init__(self, **kwargs):
                calls["client"] = kwargs
                self.models = Models()
        result = call_vertex_ai("student profile prompt", "mentor-project", "us-central1", "gemini-test-model", Client)
        self.assertEqual(result, "grounded mentoring output")
        self.assertEqual(calls["client"], {"vertexai": True, "project": "mentor-project", "location": "us-central1"})
        self.assertEqual(calls["generate"], {"model": "gemini-test-model", "contents": "student profile prompt"})

    def test_provider_failures_are_not_silently_converted_to_live_output(self):
        class FailingClient:
            def __init__(self, **kwargs):
                raise RuntimeError("provider unavailable")
        with self.assertRaisesRegex(RuntimeError, "provider unavailable"):
            call_vertex_ai("prompt", "project", "location", "model", FailingClient)

if __name__ == "__main__":
    unittest.main()
