import os
from dotenv import load_dotenv

load_dotenv()

try:
    from google import genai
except ImportError:
    genai = None


SYSTEM_INSTRUCTION = """
You are LegalEase, an AI assistant for drafting legal-document templates.
Produce a professional, editable document based only on the information supplied by the user.
Do not invent names, dates, amounts, addresses, statutes, case law, or other facts.
Use placeholders such as [MISSING INFORMATION] when important information is absent.
Organize the document with a title, numbered sections, clear clauses, and a signature section.
Write neutral, formal legal drafting language.
This is a drafting aid, not legal advice. Do not claim that the document is legally valid,
enforceable, or appropriate for a particular jurisdiction unless the user supplied that basis.
"""


class GeminiDocumentGenerator:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()

        if not self.api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured. Copy .env.example to .env and add your API key."
            )
        if genai is None:
            raise RuntimeError(
                "The google-genai package is missing. Run: pip install -r requirements.txt"
            )

        self.client = genai.Client(api_key=self.api_key)

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str,
        jurisdiction: str = "Not specified",
        additional_instructions: str = "",
    ) -> str:
        prompt = f"""
{SYSTEM_INSTRUCTION}

Draft a {document_type}.

PARTIES:
{parties}

TERMS / CONDITIONS:
{terms}

EFFECTIVE DATE:
{effective_date}

JURISDICTION:
{jurisdiction}

ADDITIONAL INSTRUCTIONS:
{additional_instructions or "None"}

Return only the document text. Do not wrap it in Markdown code fences.
"""

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
            )
        except Exception as exc:
            raise RuntimeError(f"Gemini API request failed: {exc}") from exc

        text = getattr(response, "text", None)
        if not text or not text.strip():
            raise RuntimeError("Gemini returned an empty response.")

        return sanitize_text(text)


def sanitize_text(text: str) -> str:
    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u00a0": " ",
        "\u2022": "-",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text.strip()
