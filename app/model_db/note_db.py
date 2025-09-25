from sqlalchemy import Column, Integer, String, Text, Time, DateTime, ForeignKey
from datetime import datetime
from app.database.database import Base
class Note(Base):
    __tablename__ = "note"

    id_note = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey("user.user_id", ondelete="CASCADE"), nullable=False)
    hari = Column(String(20), nullable=True)
    jam = Column(Time, nullable=True)
    judul_note = Column(String(200), nullable=False)
    description_note = Column(Text, nullable=True)
    create_at = Column(DateTime, default=datetime.utcnow)