from pydantic import BaseModel, constr
from datetime import date
from typing import Optional

class User(BaseModel):
    username: str
    password: constr(min_length=6, max_length=72)
    tanggal_lahir: date
    pekerjaan: Optional[str] = None
    jam_tidur: Optional[str] = None   # bisa diubah ke time kalau format fix (HH:MM)
    jam_kerja: Optional[str] = None   # sama, bisa pakai time
    punya_keluarga: Optional[bool] = None
    agama: Optional[str] = None

