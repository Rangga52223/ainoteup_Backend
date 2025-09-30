from pydantic import BaseModel, constr
from datetime import date, time
from typing import Optional, List

class User(BaseModel):
    username: str
    password: constr(min_length=6, max_length=72)
    tanggal_lahir: date
    pekerjaan: Optional[str] = None
    jam_tidur: Optional[str] = None   # bisa diubah ke time kalau format fix (HH:MM)
    jam_kerja: Optional[str] = None   # sama, bisa pakai time
    punya_keluarga: Optional[bool] = None
    agama: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str

class NoteCreate(BaseModel):
    hari: str | None = None
    jam: str | None = None   # format "HH:MM:SS"
    judul_note: str
    description_note: str | None = None

class NoteUpdate(BaseModel):
    hari: Optional[str] = None
    jam: Optional[time] = None
    judul_note: Optional[str] = None
    description_note: Optional[str] = None

class Ask(BaseModel):
    pertanyaan: str

class NotesBulkCreate(BaseModel):
    notes: List[NoteCreate]
