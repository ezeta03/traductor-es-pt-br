from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
import os
from uuid import uuid4
from app.worker_task import translate_file_task
from pydantic import BaseModel
from app.translator_service import translate_text

app = FastAPI()

# ====== ENDPOINT DE TEXTO ======
class TranslationRequest(BaseModel):
    text: str
    source: str = "en"
    target: str = "es"

@app.post("/translate_text")
def translate_text_endpoint(req: TranslationRequest):
    translated = translate_text(req.text, req.source, req.target)
    return {
        "original": req.text,
        "source": req.source,
        "target": req.target,
        "translated": translated
    }


# ====== ENDPOINT DE DOCUMENTOS ======
UPLOAD_DIR = os.environ.get("UPLOAD_DIR", "/data/uploads")
OUT_DIR = os.environ.get("OUT_DIR", "/data/out")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

@app.post("/translate-docx/")
async def translate_docx_endpoint(
    file: UploadFile = File(...),
    source: str = Form("en"),
    target: str = Form("es")
):
    uid = str(uuid4())
    infile = os.path.join(UPLOAD_DIR, f"{uid}_{file.filename}")
    outname = os.path.join(OUT_DIR, f"{uid}_translated.docx")

    # Guardar archivo subido
    with open(infile, "wb") as f:
        f.write(await file.read())

    # Llamar a Celery task
    task = translate_file_task.delay(infile, outname, source, target)

    return {"task_id": task.id, "status": "processing"}


# ====== ENDPOINT PARA DESCARGAR ======
@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(OUT_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(
            path=file_path,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename=filename
        )
    return {"status": "error", "error": "Archivo no encontrado"}
