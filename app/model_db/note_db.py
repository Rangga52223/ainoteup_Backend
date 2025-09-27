from sqlalchemy import Column, Integer, String, Text, Time, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from app.database.database import Base
import uuid
class Note(Base):
    __tablename__ = "note"

    id_note = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_user = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    hari = Column(String(20), nullable=True)
    jam = Column(Time, nullable=True)
    judul_note = Column(String(200), nullable=False)
    description_note = Column(Text, nullable=True)
    create_at = Column(DateTime, default=datetime.utcnow)