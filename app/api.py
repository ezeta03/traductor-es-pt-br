from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import shutil, os
from uuid import uuid4
from worker_task import translate_file_task

app = FastAPI()
UPLOAD_DIR = os.environ.get("UPLOAD_DIR", "/data/uploads")
OUT_DIR = os.environ.get("OUT_DIR", "/data/out")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

@app.post("/translate")
async def translate_endpoint(file: UploadFile = File(...)):
    uid = str(uuid4())
    infile = os.path.join(UPLOAD_DIR, f"{uid}_{file.filename}")
    outname = os.path.join(OUT_DIR, f"{uid}_translated.docx")

    # Guardar archivo subido
    with open(infile, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Ejecutar traducción (sin Celery para respuesta directa)
    result = translate_file_task(infile, outname)

    if result.get("status") == "ok":
        return FileResponse(
            path=outname,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename=f"{os.path.splitext(file.filename)[0]}_translated.docx"
        )
    else:
        return {"status": "error", "error": result.get("error")}
