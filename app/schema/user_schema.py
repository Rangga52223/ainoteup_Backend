from pydantic import BaseModel
from datetime import date, timedelta
from typing import Optional

class UserBase(BaseModel):
    user_name: str
    tanggal_lahir: date
    pekerjaan: Optional[str] = None
    jam_tidur: Optional[timedelta] = None
    jam_kerja: Optional[timedelta] = None
    punya_keluarga: Optional[bool] = None
    agama: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    user_id: int

    class Config:
        orm_mode = True