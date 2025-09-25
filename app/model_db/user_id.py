from sqlalchemy import Column, Integer, String, Date, Interval, Boolean
from app.database.database import Base
class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(100), nullable=False)
    tanggal_lahir = Column(Date, nullable=False)
    pekerjaan = Column(String(100))
    jam_tidur = Column(Interval)
    jam_kerja = Column(Interval)
    punya_keluarga = Column(Boolean, default=False)
    agama = Column(String(50))

    def __repr__(self):
        return f"<User(user_id={self.user_id}, name={self.user_name}, pekerjaan={self.pekerjaan})>"