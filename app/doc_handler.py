from docx import Document
import fitz  # PyMuPDF

def extract_text_from_docx(path: str):
    doc = Document(path)
    content = []
    for para in doc.paragraphs:
        runs = []
        for run in para.runs:
            runs.append(run.text)
        content.append({"runs": runs})
    return content

def translate_docx(input_path: str, output_path: str, translator_func):
    doc = Document(input_path)
    for para in doc.paragraphs:
        for run in para.runs:
            if run.text.strip():
                translated = translator_func(run.text)
                run.text = translated
    doc.save(output_path)

def extract_text_from_pdf(path: str) -> str:
    doc = fitz.open(path)
    texts = []
    for page in doc:
        texts.append(page.get_text("text"))
    return "\n".join(texts)
