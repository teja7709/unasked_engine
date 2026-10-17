import os, threading, webbrowser
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from agents import analyze
from parser import pdf_to_text

app = FastAPI()

@app.post("/analyze")
async def run(text: str = Form(None), file: UploadFile = File(None)):
    doc = pdf_to_text(file.file) if file else text
    return analyze(doc)

# Serves frontend/index.html at http://127.0.0.1:8000 (keep this LAST)
FRONTEND = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/", StaticFiles(directory=FRONTEND, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    threading.Timer(1.5, lambda: webbrowser.open("http://127.0.0.1:8000")).start()
    uvicorn.run("main:app", host="127.0.0.1", port=8000)