from app.model_db.note_db import Note
from app.model_db.user_id import User
from app.database.database import SessionLocal
from fastapi import Depends, APIRouter, HTTPException
from datetime import datetime, time
import uuid
db = SessionLocal()
def get_notes(current_user):
    notes = db.query(Note).filter(Note.id_user == current_user).all()
    return {"user_id": current_user, "notes": notes}

def create_note(
    note,
    current_user  # dapet dari token
):
    print(note)
    # konversi jam string → time object
    jam_value = None
    if note.jam:
        try:
            jam_value = datetime.strptime(note.jam, "%H:%M:%S").time()
        except ValueError:
            raise HTTPException(status_code=400, detail="Format jam harus HH:MM:SS")

    new_note = Note(
        id_note=uuid.uuid4(),
        id_user=current_user,
        hari=note.hari,
        jam=jam_value,
        judul_note=note.judul_note,
        description_note=note.description_note,
        create_at=datetime.utcnow(),
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return {
        "message": "Note berhasil dibuat",
        "note": {
            "id_note": new_note.id_note,
            "judul_note": new_note.judul_note,
            "description_note": new_note.description_note,
            "hari": new_note.hari,
            "jam": str(new_note.jam) if new_note.jam else None,
            "create_at": new_note.create_at,
        }
    }

def edit_note(note_id, payload, current_user):
    note = db.query(Note).filter(
        Note.id_note == note_id,
        Note.id_user == current_user  # hanya milik user tsb
    ).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note tidak ditemukan")

    update_data = payload.dict(exclude_unset=True)  # hanya field yang dikirim
    for key, value in update_data.items():
        setattr(note, key, value)

    note.create_at = datetime.utcnow()  # kalau ada kolom updated_at lebih bagus dipakai

    db.commit()
    db.refresh(note)
    return {"message": "Note berhasil diupdate", "note": note}

def delete_note(
    note_id,
    user_id, 
):
    note = db.query(Note).filter(
        Note.id_note == note_id,
        Note.id_user == user_id
    ).first()

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note tidak ditemukan atau bukan milik user"
        )

    db.delete(note)
    db.commit()

    return {"message": "Note berhasil dihapus"}