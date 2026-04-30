from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.task import Task
from app.models.notification import Notification

router = APIRouter(prefix="/kanban", tags=["Kanban"])


# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ CREATE TASK
@router.post("/tasks")
def create_task(title: str, description: str, column_id: int, db: Session = Depends(get_db)):
    task = Task(title=title, description=description, column_id=column_id)
    db.add(task)
    db.commit()
    db.refresh(task)

    # 🔔 Notification
    notif = Notification(message=f"Task '{title}' created")
    db.add(notif)
    db.commit()

    return task


# ✅ GET TASKS (Pagination + Search)
@router.get("/tasks")
def get_tasks(skip: int = 0, limit: int = 10, search: str = "", db: Session = Depends(get_db)):
    query = db.query(Task)

    if search:
        query = query.filter(Task.title.contains(search))

    tasks = query.offset(skip).limit(limit).all()
    return tasks


# ✅ DELETE TASK
@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    # 🔔 Notification
    notif = Notification(message=f"Task '{task.title}' deleted")
    db.add(notif)
    db.commit()

    return {"message": "Task deleted"}


# ✅ ANALYTICS
@router.get("/analytics")
def get_analytics(db: Session = Depends(get_db)):
    total = db.query(Task).count()
    completed = db.query(Task).filter(Task.column_id == 3).count()
    pending = total - completed

    return {
        "total": total,
        "completed": completed,
        "pending": pending
    }