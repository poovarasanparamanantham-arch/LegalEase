# LegalEase

LegalEase is an AI-powered legal document drafting application based on the supplied project specification. It uses:

- Streamlit frontend
- FastAPI backend
- Google Gemini API
- Editable document preview
- TXT, DOCX and PDF exports
- Optional logo support
- Environment-based configuration
- Automated tests

> LegalEase is a drafting aid. Generated content should be reviewed by a qualified legal professional before use.

## Project structure

```text
LegalEase/
├── backend/
│   ├── __init__.py
│   ├── __main__.py
│   ├── main.py
│   ├── routes.py
│   └── schemas.py
├── ai_core/
│   ├── __init__.py
│   └── gemini_generator.py
├── frontend/
│   └── app.py
├── utils/
│   ├── __init__.py
│   └── exporters.py
├── tests/
│   ├── test_exporters.py
│   └── test_schemas.py
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── Procfile
├── requirements.txt
└── README.md
```

## 1. VS Code setup

Install Python 3.10+ (Python 3.11 recommended) and VS Code.

Open the `LegalEase` folder in VS Code.

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 2. Configure Gemini

Copy `.env.example` to `.env`:

```text
GEMINI_API_KEY=your_real_key
gemini-3.5-flash-lite
BACKEND_URL=http://127.0.0.1:8000
```

Do not commit `.env`.

The model is configurable because model availability can change. If your Google AI account exposes a different supported Gemini model, set `GEMINI_MODEL` accordingly.

## 3. Run the backend

From the project root:

```bash
python -m uvicorn backend.main:app --reload --port 8000
```

Test:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/health
```

FastAPI docs:

```text
http://127.0.0.1:8000/docs
```

## 4. Run the frontend

Open a second VS Code terminal with the same virtual environment:

```bash
streamlit run frontend/app.py
```

Open the URL Streamlit prints, normally:

```text
http://localhost:8501
```

## 5. Test the complete app

1. Select a document type.
2. Enter parties.
3. Enter semicolon-separated terms.
4. Select the effective date.
5. Optionally add jurisdiction and extra instructions.
6. Click **Generate Document**.
7. Edit the generated text.
8. Download TXT, DOCX or PDF.

## 6. Run automated tests

```bash
pytest -q
```

These tests cover schema validation and basic TXT/DOCX/PDF generation without making a Gemini API call.

## 7. API example

POST `/generate`:

```json
{
  "document_type": "Non-Disclosure Agreement",
  "parties": "Jane Doe (Disclosing Party), TechNova Inc. (Receiving Party)",
  "terms": "Confidential information must be protected; disclosure is limited to authorized personnel; either party may terminate with 15 days notice",
  "effective_date": "2026-09-30",
  "jurisdiction": "India",
  "additional_instructions": "Use clear numbered sections."
}
```

## 8. Docker

Create `.env`, then:

```bash
docker compose up --build
```

Backend:

```text
http://localhost:8000
```

Frontend:

```text
http://localhost:8501
```

## Notes

The supplied documentation names `google-generativeai` and Gemini 1.5 Pro. This implementation uses the maintained Google `google-genai` SDK and makes the Gemini model configurable through `GEMINI_MODEL`, so the project is not hard-coded to a model that may no longer be available to a particular API account.

The document generation prompt deliberately avoids inventing legal facts and includes a legal-review notice. The application does not claim that generated documents are legally valid or enforceable.
