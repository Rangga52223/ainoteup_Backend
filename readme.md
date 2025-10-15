# 🛠 AINoteUP/NoteUP 

AINoteUP/NoteUP adalah sebuah aplikasi web yang saya buat untuk otomatisasi pembuatan note harian, fitur AI masih belum tersedia. terimakasih

---

## 📦 Instalasi & Requirement

### 1. Persiapan Environment Lokal
Pastikan sudah terinstall:
- **Python 3.10+**
- **FastApi** 
- **PostgreSql** 


### 2. Cara Instalasi
Clone repository dan install dependency:

```bash
git clone https://github.com/Rangga52223/ainoteup_Backend
cd /ainoteup_Backend
# (Opsional) Buat virtual environment
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

```

Jalankan aplikasi:
```bash
python run.py

#Kamu bisa menjalankan lewat DOCKER

#Jangan lupa setting link Database nya
```
Jika pakai docker:
```bash
docker build -t AInoteup .
```

---

## 🗄 Desain Database

**Database saya menggunakan 2 table**<br>

**-Table users**
table yang berisi informasi user seperti tanggal lahir, agama dll

**-Table Note**
table untuk menyimpan note yang sudah di buat oleh user



## 📚 Library & Framework yang Digunakan

- uvicorn==0.36.0
- fastapi==0.117.1
- python-dotenv==0.19.2
- python-jose[cryptography]==3.3.0
- passlib==1.7.4
- psycopg2-binary==2.9.9
- bcrypt==3.2.0
- SQLAlchemy==2.0.25
- alembic==1.13.1

---
## 🔥 LIST API Endpoint & Request payload
### Register
- https://ainoteup-backend.vercel.app/api/v1/auth/register
request
```json
{
  "username": "maksud1",
  "password": "rahasia123",
  "tanggal_lahir": "2001-05-17",
  "pekerjaan": "Mahasiswa",
  "jam_tidur": "23:00",
  "jam_kerja": "08:00-16:00",
  "punya_keluarga": true,
  "agama": "Islam"
}
```
response
```json
{
    "success": true,
    "message": "User registered successfully",
    "data": null
}
```
### login
- https://ainoteup-backend.vercel.app/api/v1/auth/login
request
```json
{
  "username": "maksud1",
  "password": "rahasia123"
}
```
response
```json
{
    "success": true,
    "message": "login sukses",
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZjEyYzczOTktZDhhNy00NmI1LThmYjYtOTA2MDk4MTBkMGE0IiwiZXhwIjoxNzYwNTU3NjY0fQ.aZ1hJzb_S2QH_0LCz-PCS6O4Cg0TnalZ00V1K22KhvQ",
    "user_id": "f12c7399-d8a7-46b5-8fb6-90609810d0a4"
}
```
#### ⚠ Pakai Token Bearer di authentikasi untuk akses endpoint di bawah ini
### Ambil Semua Note
- https://ainoteup-backend.vercel.app/api/v1/note/
- GET
request
```json

```
response
```json
{
    "success": true,
    "message": "Notes retrieved",
    "data": {
        "userId": "f12c7399-d8a7-46b5-8fb6-90609810d0a4",
        "notes": [
            {
                "idNote": "bc3802d0-08c8-4cef-bf66-f4e616ea074b",
                "idUser": "f12c7399-d8a7-46b5-8fb6-90609810d0a4",
                "hari": 5,
                "jam": "10:00:00",
                "judulNote": "Rapat penggunaan Uang Perusahaan",
                "descriptionNote": "Membahas tentang Kemajuan Perusahann",
                "createAt": "2025-10-15T18:49:48.191561"
            },
            {
                "idNote": "391866be-ff3f-4451-ac23-7cfa0032f812",
                "idUser": "f12c7399-d8a7-46b5-8fb6-90609810d0a4",
                "hari": 4,
                "jam": "10:00:00",
                "judulNote": "Rapat penggunaan Uang Perusahaan",
                "descriptionNote": "Membahas tentang Kemajuan Perusahann",
                "createAt": "2025-10-15T18:53:34.945134"
            }
        ]
    }
}
```
### ambil detail note
- https://ainoteup-backend.vercel.app/api/v1/note/detail-note/{id_note}
- GET
request
```json

```
response
```json
{
    "success": true,
    "message": "Note detail retrieved",
    "data": {
        "note": {
            "idNote": "391866be-ff3f-4451-ac23-7cfa0032f812",
            "idUser": "f12c7399-d8a7-46b5-8fb6-90609810d0a4",
            "hari": 4,
            "jam": "10:00:00",
            "judulNote": "Rapat penggunaan Uang Perusahaan",
            "descriptionNote": "Membahas tentang Kemajuan Perusahann",
            "createAt": "2025-10-15T18:53:34.945134"
        }
    }
}
```
### ambil detail note
- https://ainoteup-backend.vercel.app/api/v1/note/add-note
- POST
request
```json
{
  "hari": "4",
  "jam": "10:00:00",
  "judul_note": "Rapat penggunaan Uang Perusahaan",
  "description_note": "Membahas tentang Kemajuan Perusahann"
}
```
response
```json
{
    "success": true,
    "message": "Note berhasil dibuat",
    "data": {
        "note": {
            "idNote": "391866be-ff3f-4451-ac23-7cfa0032f812",
            "idUser": "f12c7399-d8a7-46b5-8fb6-90609810d0a4",
            "hari": 4,
            "jam": "10:00:00",
            "judulNote": "Rapat penggunaan Uang Perusahaan",
            "descriptionNote": "Membahas tentang Kemajuan Perusahann",
            "createAt": "2025-10-15T18:53:34.945134"
        }
    }
}
```

## 📄 Lisensi
MIT License – bebas digunakan dan dimodifikasi.
