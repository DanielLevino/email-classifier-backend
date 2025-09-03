from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
from classifier import classify_email, extract_text_from_file

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EmailRequest(BaseModel):
    text: str

@app.post("/process_email")
async def process_email(data: EmailRequest):
    categoria, resposta = classify_email(data.text)
    return {"categoria": categoria, "resposta": resposta}

@app.post("/process_file")
async def process_file(file: UploadFile = File(...)):
    contents = await file.read()
    text = extract_text_from_file(file=bytes(contents), filename=file.filename)
    categoria, resposta = classify_email(text)
    return {"categoria": categoria, "resposta": resposta, "texto_extraido": text}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
