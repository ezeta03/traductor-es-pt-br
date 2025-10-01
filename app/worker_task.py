from celery import Celery
from docx import Document
import os

# Configurar Celery
celery = Celery(
    "worker_task",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

@celery.task
def translate_text(text: str) -> str:
    """
    Traducción simulada de un texto. Aquí puedes integrar tu API real
    de traducción (DeepL, Hugging Face, etc.).
    """
    return f"{text} (traducido al portugués)"

@celery.task
def translate_file_task(input_path: str, output_path: str):
    """
    Traduce un archivo DOCX manteniendo el formato y estilos.
    """
    if not os.path.exists(input_path):
        return {"status": "error", "error": "Archivo de entrada no existe"}

    # Abrir el DOCX
    doc = Document(input_path)
    translated_doc = Document()

    # Traducir cada párrafo manteniendo estilos
    for para in doc.paragraphs:
        # Traducir el texto (simulación o API real)
        text = para.text.strip()
        translated_text = translate_text(text) if text else ""

        # Crear nuevo párrafo en documento traducido
        p = translated_doc.add_paragraph()
        run = p.add_run(translated_text)

        # Mantener estilo de cada run
        for r_src, r_dest in zip(para.runs, p.runs):
            r_dest.bold = r_src.bold
            r_dest.italic = r_src.italic
            r_dest.underline = r_src.underline
            r_dest.font.name = r_src.font.name
            r_dest.font.size = r_src.font.size

    # Guardar el archivo traducido
    translated_doc.save(output_path)

    return {"status": "ok"}
