import pytest
from pydantic import ValidationError

from backend.schemas import DocumentRequest


def test_valid_request():
    request = DocumentRequest(
        document_type="NDA",
        parties="A and B",
        terms="Keep information confidential",
        effective_date="2026-09-30",
    )
    assert request.document_type == "NDA"


def test_empty_required_field_rejected():
    with pytest.raises(ValidationError):
        DocumentRequest(
            document_type="NDA",
            parties="",
            terms="term",
            effective_date="today",
        )
