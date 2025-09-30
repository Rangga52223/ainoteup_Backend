from app.route import note
from fastapi import Depends, HTTPException
from app.middleware.auth import session_checking
from app.service.note_service import get_notes, create_note, edit_note, delete_note
from app.helper.pydantict_helper import NoteCreate, NoteUpdate
from uuid import UUID

@note.get('/')
async def get_note_route(user: str = Depends(session_checking)):
    try:
        return get_notes(user)
    except Exception as e:
        print(f'Debug_Error:{str(e)}')
        return HTTPException(status_code=400, detail=f'Error di get_notes_route:{str(e)}')

@note.post('/add-note')
async def add_note_route(note: NoteCreate, user: str = Depends(session_checking)):
    try:
        return create_note(note, user)
    except Exception as e:
        print(f'Debug_Error:{str(e)}')
        return HTTPException(status_code=400, detail=f'Error di add_note_route:{str(e)}')
    
@note.put('/edit-note/{note_id}')
async def edit_note_route(note_id: UUID, note_data:NoteUpdate, user = Depends(session_checking)):
    try:
        return edit_note(note_id, note_data, user)
    except Exception as e:
        print(f'Debug_Error:{str(e)}')
        return HTTPException(status_code=400, detail=f'Error di edit_note_route:{str(e)}')
    
@note.delete('/delete-note/{note_id}')
async def delete_note_route(note_id: UUID, user = Depends(session_checking)):
    try:
        return delete_note(note_id, user)
    except Exception as e:
        print(f'Debug_Error:{str(e)}')
        return HTTPException(status_code=400, detail=f'Error di delete_note_route:{str(e)}')