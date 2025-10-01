from googletrans import Translator
from celery import Celery
from docx import Document
import os

celery = Celery(
    "worker_task",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

translator = Translator()

@celery.task
def translate_text(text: str) -> str:
    if not text.strip():
        return ""
    result = translator.translate(text, src="es", dest="pt")
    return result.text

@celery.task
def translate_file_task(input_path: str, output_path: str):
    if not os.path.exists(input_path):
        return {"status": "error", "error": "Archivo no existe"}

    doc = Document(input_path)
    translated_doc = Document()

    for para in doc.paragraphs:
        text = para.text.strip()
        translated_text = translate_text(text)
        p = translated_doc.add_paragraph()
        run = p.add_run(translated_text)
        for r_src, r_dest in zip(para.runs, p.runs):
            r_dest.bold = r_src.bold
            r_dest.italic = r_src.italic
            r_dest.underline = r_src.underline
            r_dest.font.name = r_src.font.name
            r_dest.font.size = r_src.font.size

    translated_doc.save(output_path)
    return {"status": "ok"}
