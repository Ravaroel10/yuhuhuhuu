from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import yagmail

app = FastAPI()

# Aktifkan CORS agar bisa akses dari frontend (misal IP lain)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ganti dengan domain/frontend kamu kalau mau lebih aman
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Simpan foto sementara
    with open("photo.png", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Kirim ke Gmail
    yag = yagmail.SMTP("rafaelgul0001@gmail.com", "rafael100609")
    yag.send(
        to="rafa100609@gmail.com",
        subject="📸 Foto dari Web Photobooth",
        contents="Hai! Ini foto hasil jepretan user via web photobooth 😊",
        attachments="photo.png"
    )

    return {"message": "Foto berhasil dikirim ke email!"}
