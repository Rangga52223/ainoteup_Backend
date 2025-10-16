# 🛠 AINoteUP / NoteUP

AINoteUP / NoteUP adalah aplikasi web untuk otomatisasi pembuatan catatan harian. Fitur AI belum tersedia saat ini. (Public Endpoint ada di bagian 🔥 API Endpoints )

---

## 📦 Instalasi & Persyaratan

### Persyaratan
- Python 3.10+
- PostgreSQL
- (Opsional) Docker

### Langkah instalasi
1. Clone repository:
```bash
git clone https://github.com/Rangga52223/ainoteup_Backend.git
cd ainoteup_Backend
```

2. (Opsional) Buat dan aktifkan virtual environment:
```bash
# Linux / macOS
python -m venv venv
source venv/bin/activate

# Windows (PowerShell)
python -m venv venv
venv\Scripts\Activate.ps1
```

3. Install dependency:
```bash
pip install -r requirements.txt
```

4. Buat file .env dan atur variabel lingkungan (contoh: DATABASE_URL).

5. Jalankan aplikasi:
```bash
python run.py
# atau (jika menggunakan uvicorn)
uvicorn run:app --reload
```

#### Menggunakan Docker
Build image:
```bash
docker build -t ainoteup-backend .
```
Jalankan container (contoh):
```bash
docker run -e DATABASE_URL="postgres://user:pass@host:5432/db" -p 8000:8000 ainoteup-backend
```

---

## 🗄 Desain Database

Database menggunakan dua tabel utama:

- users — menyimpan data pengguna (username, tanggal_lahir, pekerjaan, dll.)
- notes — menyimpan catatan pengguna (hari, jam, judul, deskripsi, created_at)

---

## 📚 Dependensi utama

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

## 🔥 API Endpoints (Ringkasan)

Base URL: https://ainoteup-backend.vercel.app/api/v1

Catatan: Gunakan Bearer Token pada header Authorization untuk endpoint yang membutuhkan otentikasi.

### Register
- POST /auth/register <br>
Request:
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
Response:
```json
{
    "success": true,
    "message": "User registered successfully",
    "data": null
}
```

### Login
- POST /auth/login  <br>
Request:
```json
{
    "username": "maksud1",
    "password": "rahasia123"
}
```
Response:
```json
{
    "success": true,
    "message": "login sukses",
    "access_token": "...",
    "user_id": "f12c7399-..."
}
```

### Ambil Semua Note
- GET /note/ <br>
Request: (Bearer token)
Response contoh:
```json
{
    "success": true,
    "message": "Notes retrieved",
    "data": {
        "userId": "f12c7399-...",
        "notes": [
            {
                "idNote": "bc3802d0-...",
                "idUser": "f12c7399-...",
                "hari": 5,
                "jam": "10:00:00",
                "judulNote": "Rapat penggunaan Uang Perusahaan",
                "descriptionNote": "Membahas tentang Kemajuan Perusahaan",
                "createAt": "2025-10-15T18:49:48.191561"
            }
        ]
    }
}
```

### Ambil Detail Note
- GET /note/detail-note/{id_note}<br>
Request: (Bearer token)
Response contoh:
```json
{
    "success": true,
    "message": "Note detail retrieved",
    "data": {
        "note": {
            "idNote": "391866be-...",
            "idUser": "f12c7399-...",
            "hari": 4,
            "jam": "10:00:00",
            "judulNote": "Rapat penggunaan Uang Perusahaan",
            "descriptionNote": "Membahas tentang Kemajuan Perusahaan",
            "createAt": "2025-10-15T18:53:34.945134"
        }
    }
}
```

### Tambah Note
- POST /note/add-note<br>
Request (Bearer token):
```json
{
    "hari": "4",
    "jam": "10:00:00",
    "judul_note": "Rapat penggunaan Uang Perusahaan",
    "description_note": "Membahas tentang Kemajuan Perusahaan"
}
```
Response contoh:
```json
{
    "success": true,
    "message": "Note berhasil dibuat",
    "data": {
        "note": {
            "idNote": "391866be-...",
            "idUser": "f12c7399-...",
            "hari": 4,
            "jam": "10:00:00",
            "judulNote": "Rapat penggunaan Uang Perusahaan",
            "descriptionNote": "Membahas tentang Kemajuan Perusahaan",
            "createAt": "2025-10-15T18:53:34.945134"
        }
    }
}
```

### Edit Note
- PUT /note/edit-note/{id-note}<br>
Request (Bearer token):
```json
{
  "hari": "Senin",
  "jam": "10:30:00",
  "judul_note": "Rapat Tim Tahunan",
  "description_note": "Membahas progres proyek dan rencana untuk minggu depan."
}
```
Response contoh:
```json
{
    "success": true,
    "message": "Note berhasil diupdate",
    "data": {
        "note": {
            "idNote": "391866be-...",
            "idUser": "f12c7399-...",
            "hari": 4,
            "jam": "10:00:00",
            "judulNote": "Rapat penggunaan Uang Perusahaan",
            "descriptionNote": "Membahas tentang Kemajuan Perusahaan",
            "createAt": "2025-10-15T18:53:34.945134"
        }
    }
}
```
### Delete Note
- DELETE /note/delete-note/{id-note}<br>
Request (Bearer token):
```json

```
Response contoh:
```json
{
    "success": true,
    "message": "Note berhasil dihapus",
    "data": null
}
```

### Logout 
- POST /auth/logout <br>
Request (Bearer token):
```json

```
Response contoh:
```json
{
    "success": true,
    "message": "Logout successful",
    "data": null
}
```

---

## 📄 Lisensi

MIT License — bebas digunakan dan dimodifikasi.

--- 

Catatan: Periksa konfigurasi DATABASE_URL dan variabel lingkungan lain sebelum menjalankan aplikasi.
