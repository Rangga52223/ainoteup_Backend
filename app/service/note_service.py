from app.model_db.note_db import Note
from app.model_db.user_id import User
from app.response.base_response import succes_response, error_response
from app.database.database import SessionLocal
from fastapi import Depends, APIRouter, HTTPException
from datetime import datetime, time
import uuid
from typing import Any

db = SessionLocal()

def _day_to_number(value: Any) -> int | None:
    """
    Terima angka (int atau str digit) dan kembalikan int 1..7.
    Kembalikan None jika tidak valid.
    """
    if value is None:
        return None
    if isinstance(value, int):
        return value if 1 <= value <= 7 else None
    if isinstance(value, str):
        s = value.strip()
        if s.isdigit():
            n = int(s)
            return n if 1 <= n <= 7 else None
    return None

def _serialize_note(n: Note):
    return {
        "idNote": str(n.id_note),
        "idUser": str(n.id_user),
        "hari": int(n.hari) if n.hari is not None and str(n.hari).isdigit() else None,
        "jam": str(n.jam) if n.jam else None,
        "judulNote": n.judul_note,
        "descriptionNote": n.description_note,
        "createAt": n.create_at.isoformat() if n.create_at else None
    }

def get_notes(current_user):
    try:
        current_user_uuid = uuid.UUID(current_user)
        notes = db.query(Note).filter(Note.id_user == current_user_uuid).all()
        notes_list = [_serialize_note(n) for n in notes]
        return succes_response(http_status=200, message="Notes retrieved", data={
            "userId": str(current_user_uuid),
            "notes": notes_list
        })
    except ValueError:
        return error_response(http_status=400, message="Invalid user id")
    except Exception as e:
        print(f"Debug_Error:{str(e)}")
        return error_response(http_status=500, message="Failed to get notes")

def get_note_detail(note_id, current_user):
    try:
        current_user_uuid = uuid.UUID(current_user)
        note = db.query(Note).filter(
            Note.id_note == note_id,
            Note.id_user == current_user_uuid
        ).first()
        if not note:
            return error_response(http_status=404, message="Note tidak ditemukan")
        return succes_response(http_status=200, message="Note detail retrieved", data={"note": _serialize_note(note)})
    except ValueError:
        return error_response(http_status=400, message="Invalid user id")
    except Exception as e:
        print(f"Debug_Error:{str(e)}")
        return error_response(http_status=500, message="Failed to get note detail")

def create_note(
    note,
    current_user  
):
    try:
        current_user_uuid = uuid.UUID(current_user)
    except ValueError:
        return error_response(http_status=400, message="Invalid user id")

    jam_value = None
    if getattr(note, "jam", None):
        try:
            jam_value = datetime.strptime(note.jam, "%H:%M:%S").time()
        except ValueError:
            return error_response(http_status=400, message="Format jam harus HH:MM:SS")

    hari_num = _day_to_number(getattr(note, "hari", None))
    if getattr(note, "hari", None) is not None and hari_num is None:
        return error_response(http_status=400, message="Field 'hari' tidak valid. Gunakan angka 1..7.")

    new_note = Note(
        id_note=uuid.uuid4(),
        id_user=current_user_uuid,
        hari=str(hari_num) if hari_num is not None else None,
        jam=jam_value,
        judul_note=note.judul_note,
        description_note=note.description_note,
        create_at=datetime.utcnow(),
    )
    try:
        db.add(new_note)
        db.commit()
        db.refresh(new_note)
    except Exception as e:
        db.rollback()
        print(f"Debug_Error:{str(e)}")
        return error_response(http_status=500, message="Gagal membuat note")

    return succes_response(
        http_status=201,
        message="Note berhasil dibuat",
        data={
            "note": _serialize_note(new_note)
        }
    )

def edit_note(note_id, payload, current_user):
    try:
        current_user_uuid = uuid.UUID(current_user)
    except ValueError:
        return error_response(http_status=400, message="Invalid user id")

    note = db.query(Note).filter(
        Note.id_note == note_id,
        Note.id_user == current_user_uuid  
    ).first()
    if not note:
        return error_response(http_status=404, message="Note tidak ditemukan")

    update_data = payload.dict(exclude_unset=True)  

    if "jam" in update_data and update_data["jam"] is not None:
        try:
            update_data["jam"] = datetime.strptime(update_data["jam"], "%H:%M:%S").time()
        except ValueError:
            return error_response(http_status=400, message="Format jam harus HH:MM:SS")

    if "hari" in update_data:
        hari_num = _day_to_number(update_data["hari"])
        if update_data["hari"] is not None and hari_num is None:
            return error_response(http_status=400, message="Field 'hari' tidak valid. Gunakan angka 1..7.")
        update_data["hari"] = str(hari_num) if hari_num is not None else None

    for key, value in update_data.items():
        setattr(note, key, value)
    note.create_at = datetime.utcnow()
    try:
        db.commit()
        db.refresh(note)
    except Exception as e:
        db.rollback()
        print(f"Debug_Error:{str(e)}")
        return error_response(http_status=500, message="Gagal mengupdate note")

    return succes_response(http_status=200, message="Note berhasil diupdate", data={"note": _serialize_note(note)})

def delete_note(
    note_id,
    user_id,
):
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        return error_response(http_status=400, message="Invalid user id")

    note = db.query(Note).filter(
        Note.id_note == note_id,
        Note.id_user == user_uuid
    ).first()

    if not note:
        return error_response(http_status=404, message="Note tidak ditemukan atau bukan milik user")

    try:
        db.delete(note)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Debug_Error:{str(e)}")
        return error_response(http_status=500, message="Gagal menghapus note")

    return succes_response(http_status=200, message="Note berhasil dihapus")