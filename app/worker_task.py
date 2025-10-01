from doc_handler import translate_docx, extract_text_from_pdf
from translate_service import translate_text

def translate_file_task(input_path: str, out_path: str, glossary: dict = None, options: dict = None):
    try:
        if input_path.lower().endswith(".docx"):
            translate_docx(input_path, out_path, translate_text)
        elif input_path.lower().endswith(".pdf"):
            text = extract_text_from_pdf(input_path)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(translate_text(text))
        else:
            with open(input_path, "r", encoding="utf-8") as f:
                text = f.read()
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(translate_text(text))
        return {"status": "ok", "out_path": out_path}
    except Exception as e:
        return {"status": "error", "error": str(e)}
