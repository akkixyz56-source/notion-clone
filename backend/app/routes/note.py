from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.note import NoteCreate, NoteUpdate
from app.models.note import Note
from app.models.note_version import NoteVersion
from app.db.deps import get_db
from app.core.deps import get_current_user
from app.services.permissions import check_workspace_access
from app.models.user import User

router = APIRouter(prefix="/notes", tags=["Notes"])


# 👉 Create Note
@router.post("/")
def create_note(data: NoteCreate,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):

    check_workspace_access(db, current_user.id, data.workspace_id)

    note = Note(
        workspace_id=data.workspace_id,
        content=data.content
    )

    db.add(note)
    db.commit()
    db.refresh(note)

    # save first version
    version = NoteVersion(
        note_id=note.id,
        content=data.content
    )
    db.add(version)
    db.commit()

    return note


# 👉 Get Notes
@router.get("/{workspace_id}")
def get_notes(workspace_id: int,
              db: Session = Depends(get_db),
              current_user: User = Depends(get_current_user)):

    check_workspace_access(db, current_user.id, workspace_id)

    notes = db.query(Note).filter(
        Note.workspace_id == workspace_id
    ).all()

    return notes


# 👉 Update Note
@router.put("/{note_id}")
def update_note(note_id: int,
                data: NoteUpdate,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):

    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    check_workspace_access(db, note.workspace_id, current_user.id)

    # save old version
    version = NoteVersion(
        note_id=note.id,
        content=note.content
    )
    db.add(version)

    # update note
    note.content = data.content
    db.commit()

    return {"message": "Note updated scuccessfully"}


# 👉 Delete Note
@router.delete("/{note_id}")
def delete_note(note_id: int,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):

    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    check_workspace_access(db, note.workspace_id, current_user.id)

    db.delete(note)
    db.commit()

    return {"message": "Note deleted"}


# 👉 Get Version History
@router.get("/{note_id}/history")
def get_note_history(note_id: int,
                     db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user)):

    versions = db.query(NoteVersion).filter(
        NoteVersion.note_id == note_id
    ).all()

    return versions