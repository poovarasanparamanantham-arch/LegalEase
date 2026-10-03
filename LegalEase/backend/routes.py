from fastapi import APIRouter, HTTPException
from backend.schemas import DocumentRequest, DocumentResponse
from ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter()
generator = GeminiDocumentGenerator()


@router.post("/generate", response_model=DocumentResponse, tags=["documents"])
def generate_document(request: DocumentRequest):
    try:
        content = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            effective_date=request.effective_date,
            jurisdiction=request.jurisdiction,
            additional_instructions=request.additional_instructions,
        )
        return DocumentResponse(
            document_type=request.document_type,
            content=content,
            model=generator.model_name,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Document generation failed.") from exc
