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


   ```
## 📄 Lisensi
MIT License – bebas digunakan dan dimodifikasi.
