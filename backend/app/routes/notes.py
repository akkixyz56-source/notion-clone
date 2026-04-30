from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.note import Note

router = APIRouter()

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ Create Note
@router.post("/")
def create_note(title: str, content: str, db: Session = Depends(get_db)):
    note = Note(title=title, content=content)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


# ✅ Get Notes (with pagination)
@router.get("/{workspace_id}")
def get_notes(
    workspace_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    notes = db.query(Note).offset(skip).limit(limit).all()
    return notes


# ✅ Update Note
@router.put("/{note_id}")
def update_note(
    note_id: int,
    title: str,
    content: str,
    db: Session = Depends(get_db)
):
    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        return {"error": "Note not found"}

    note.title = title
    note.content = content

    db.commit()
    db.refresh(note)
    return note


# ✅ Delete Note
@router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        return {"error": "Note not found"}

    db.delete(note)
    db.commit()

    return {"message": "Note deleted"}


# ✅ Note History (basic placeholder)
@router.get("/{note_id}/history")
def note_history(note_id: int):
    return {
        "note_id": note_id,
        "history": ["Created", "Updated"]
    }