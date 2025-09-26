from sqlalchemy import Column, Integer, String, Date, Interval, Boolean
from app.database.database import Base
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(100), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    tanggal_lahir = Column(Date, nullable=False)
    pekerjaan = Column(String(100))
    jam_tidur = Column(String(50))   # ✅ ubah ke String
    jam_kerja = Column(String(50))   # ✅ ubah ke String
    punya_keluarga = Column(Boolean, default=False)
    agama = Column(String(50))

    def __repr__(self):
        return f"<User(user_id={self.user_id}, name={self.user_name}, pekerjaan={self.pekerjaan})>"