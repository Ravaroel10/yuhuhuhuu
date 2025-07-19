from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import yagmail
import os
import uuid

app = FastAPI()

# Aktifkan CORS agar bisa akses dari frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Bisa dibatasi ke domain tertentu kalau mau lebih aman
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Generate nama file unik
    filename = f"{uuid.uuid4()}.png"
    
    # Simpan file sementara
    with open(filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Ambil kredensial dari environment variable
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASS = os.getenv("EMAIL_PASS")

    # Kirim email
    yag = yagmail.SMTP(EMAIL_USER, EMAIL_PASS)
    yag.send(
        to="rafa100609@gmail.com",  # Ganti tujuan jika perlu
        subject="📸 Foto dari Web Photobooth",
        contents="Hai! Ini foto hasil jepretan user via web photobooth 😊",
        attachments=filename
    )

    return {"message": "Foto berhasil dikirim ke email!"}
