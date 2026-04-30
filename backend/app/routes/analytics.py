from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.task import Task

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/analytics")
def get_analytics(db: Session = Depends(get_db)):
    total = db.query(Task).count()
    completed = db.query(Task).filter(Task.column_id == 3).count()
    pending = db.query(Task).filter(Task.column_id != 3).count()

    return {
        "total": total,
        "completed": completed,
        "pending": pending
    }