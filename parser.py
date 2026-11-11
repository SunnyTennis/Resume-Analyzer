from pathlib import Path
import re

def extract_text(file_bytes: bytes, filename: str) -> str:
    """Extract text from PDF, DOCX, or plain-text uploads."""
    suffix = Path(filename).suffix.lower()
    if suffix == ".pdf":
        import fitz
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text = "\n".join(page.get_text("text") for page in doc)
    elif suffix == ".docx":
        from docx import Document
        import io
        doc = Document(io.BytesIO(file_bytes))
        text = "\n".join(p.text for p in doc.paragraphs)
        for table in doc.tables:
            for row in table.rows:
                text += "\n" + " | ".join(cell.text for cell in row.cells)
    elif suffix in {".txt", ".md"}:
        text = file_bytes.decode("utf-8", errors="replace")
    else:
        raise ValueError("Unsupported file type. Upload PDF, DOCX, or TXT.")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    if not text.strip():
        raise ValueError("No readable text was found. The file may be scanned; OCR is not included.")
    return text.strip()

def extract_sections(text: str) -> dict:
    """Lightweight heading-based section extraction; keeps all text as fallback."""
    headings = {
        "skills": r"(?im)^\s*(technical\s+skills|skills|technologies)\s*:?\s*$",
        "experience": r"(?im)^\s*(professional\s+experience|work\s+experience|experience|employment)\s*:?\s*$",
        "education": r"(?im)^\s*(education|academic\s+background)\s*:?\s*$",
        "projects": r"(?im)^\s*(projects|selected\s+projects)\s*:?\s*$",
    }
    matches = []
    for name, pattern in headings.items():
        for m in re.finditer(pattern, text):
            matches.append((m.start(), m.end(), name))
    matches.sort()
    result = {k: "" for k in headings}
    for i, (start, end, name) in enumerate(matches):
        stop = matches[i+1][0] if i+1 < len(matches) else len(text)
        result[name] = text[end:stop].strip()
    result["full_text"] = text
    return result
