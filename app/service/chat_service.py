from app.LLM.llama import llm_tool_calling
import datetime
import uuid
from app.database.database import SessionLocal
from langchain.tools import StructuredTool
from app.helper.pydantict_helper import NoteCreate, NotesBulkCreate
from typing import List
from app.model_db.note_db import Note
db = SessionLocal()


def create_notes_for_llm(notes: List[NoteCreate], current_user: uuid.UUID):
    created_notes = []
    errors = []

    for idx, note_data in enumerate(notes, start=1):
        try:
            # konversi jam string -> time object
            jam_value = None
            if note_data.jam:
                try:
                    jam_value = datetime.strptime(note_data.jam, "%H:%M:%S").time()
                except ValueError:
                    errors.append({"index": idx, "error": "Format jam harus HH:MM:SS"})
                    continue

            # buat object Note (SQLAlchemy)
            new_note = Note(
                id_note=uuid.uuid4(),
                id_user=current_user,
                hari=note_data.hari,
                jam=jam_value,
                judul_note=note_data.judul_note,
                description_note=note_data.description_note,
                create_at=datetime.utcnow(),
            )
            db.add(new_note)
            created_notes.append(new_note)

        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    db.commit()
    for n in created_notes:
        db.refresh(n)

    return {
        "message": f"{len(created_notes)} note berhasil dibuat",
        "notes": [
            {
                "id_note": str(n.id_note),
                "judul_note": n.judul_note,
                "description_note": n.description_note,
                "hari": n.hari,
                "jam": str(n.jam) if n.jam else None,
                "create_at": n.create_at.isoformat(),
            }
            for n in created_notes
        ],
        "errors": errors if errors else None
    }

def make_tools(user: uuid.UUID):
    # wrapper untuk notes
    def wrapper_create_notes(notes: List[NoteCreate]):
        return create_notes_for_llm(notes, user)

    note_tool = StructuredTool.from_function(
        func=wrapper_create_notes,
        name="Note_Create",
        description="Gunakan untuk membuat note baru, bisa 1 atau banyak sekaligus. "
                    "Input harus berupa JSON dengan field notes:[hari, jam, judul_note, description_note].",
        args_schema=NotesBulkCreate
    )


    return [note_tool]  # tinggal tambah aja


def Asked_AI(ask, user):
    propmt = f'''Kamu adalah AI Asisten aplikasi note, Jawab pertanyaan dari {ask.pertanyaan}.
    Data yang penting:
    Current_user:{user}.
    Jawab sesuai permintaan user.'''
    tools = make_tools(user)
    answer = llm_tool_calling(tools, propmt)
    return {'Answer' : answer}