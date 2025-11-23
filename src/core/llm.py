import os
import google.generativeai as genai
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()


# --- Modèles de Données ---
class TestPlan(BaseModel):
    explanation: str = Field(..., description="Why this test reveals the bug.")
    test_code: str = Field(
        ..., description="Complete python code using pytest including imports."
    )


class PatchPlan(BaseModel):
    explanation: str = Field(..., description="What was fixed.")
    fixed_code: str = Field(..., description="The full fixed python file content.")


# --- Moteur IA ---
class LLMEngine:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY manquante dans .env")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def generate_reproduction_test(self, source_code: str) -> TestPlan:
        prompt = f"""
        You are a QA Engineer. Analyze code, find bugs, write a failing Pytest script.
        
        CRITICAL: The test code MUST include the source code directly (copy-paste it at the top).
        DO NOT use import statements. The test will run in an isolated environment.
        
        Code to test:
        ```python
        {source_code}
        ```
        
        Your test_code should follow this structure:
        ```python
        # Copy the source code here (the functions to test)
        def function_name(...):
            ...
        
        # Then write pytest tests
        import pytest
        
        def test_something():
            assert function_name(...) == expected
        ```
        
        Return JSON matching this schema:
        {{
            "explanation": "string (explain what bug you found)",
            "test_code": "string (complete pytest code with source included)"
        }}
        """

        response = self.model.generate_content(
            prompt, generation_config={"response_mime_type": "application/json"}
        )
        return TestPlan.model_validate_json(response.text)

    def _clean_json(self, text: str) -> str:
        """Nettoie le texte pour extraire le JSON."""
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()

    def generate_patch(
        self, source_code: str, test_code: str, error_log: str
    ) -> PatchPlan:
        prompt = f"""
        You are a Senior Dev. Fix the code so the test passes. Return FULL code.
        
        Source:
        {source_code}
        
        Test:
        {test_code}
        
        Error:
        {error_log}
        
        Return JSON matching this schema:
        {{
            "explanation": "string",
            "fixed_code": "string"
        }}
        """

        response = self.model.generate_content(
            prompt, generation_config={"response_mime_type": "application/json"}
        )
        return PatchPlan.model_validate_json(self._clean_json(response.text))
