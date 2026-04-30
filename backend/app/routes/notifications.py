from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.notification import Notification
from app.db.database import Base

router = APIRouter(tags=["Notifications"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🔔 Create Notification
@router.post("/")
def create_notification(message: str, db: Session = Depends(get_db)):
    notif = Notification(message=message)
    db.add(notif)
    db.commit()
    db.refresh(notif)
    return notif


# 🔔 Get Notifications
@router.get("/")
def get_notifications(db: Session = Depends(get_db)):
    return db.query(Notification).order_by(Notification.id.desc()).all()


# 🔔 Mark as read
@router.put("/{id}")
def mark_read(id: int, db: Session = Depends(get_db)):
    notif = db.query(Notification).filter(Notification.id == id).first()
    if notif:
        notif.status = "read"
        db.commit()
    return notif