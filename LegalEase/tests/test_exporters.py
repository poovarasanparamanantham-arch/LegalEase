from utils.exporters import text_to_txt, format_docx, format_pdf


def test_txt_export():
    assert text_to_txt("Hello").decode("utf-8") == "Hello"


def test_docx_export():
    data = format_docx("1. Confidentiality\nThe parties agree.", "NDA")
    assert data[:2] == b"PK"


def test_pdf_export():
    data = format_pdf("1. Confidentiality\nThe parties agree.", "NDA")
    assert data.startswith(b"%PDF")
