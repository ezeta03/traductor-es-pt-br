from googletrans import Translator
from docx import Document
import os

translator = Translator()

def translate_file(input_path: str, output_path: str):
    doc = Document(input_path)
    translated_doc = Document()

    for para in doc.paragraphs:
        text = para.text
        if text.strip():
            translated_text = translator.translate(text, src="es", dest="pt").text
        else:
            translated_text = ""

        # Agregar párrafo traducido
        p_new = translated_doc.add_paragraph(translated_text)

        # Copiar estilos básicos
        if para.runs:
            for run_src, run_dest in zip(para.runs, p_new.runs):
                run_dest.bold = run_src.bold
                run_dest.italic = run_src.italic
                run_dest.underline = run_src.underline
                if run_src.font.name:
                    run_dest.font.name = run_src.font.name
                if run_src.font.size:
                    run_dest.font.size = run_src.font.size

    translated_doc.save(output_path)
    return {"status": "ok"}
