from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models import Board, Column, Task
from app.services.websocket.manager import manager
from app.db.deps import get_db
from fastapi import Depends

router = APIRouter()


# =========================
# DB Dependency
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# BOARDS
# =========================

@router.post("/boards")
async def create_board(board: dict):
    db = SessionLocal()

    new_board = Board(
        name=board["name"],
        workspace_id=board["workspace_id"]
    )

    db.add(new_board)
    db.commit()
    db.refresh(new_board)

    return new_board


@router.get("/boards")
async def get_boards():
    db = SessionLocal()
    boards = db.query(Board).all()
    return boards


# =========================
# COLUMNS
# =========================

@router.post("/columns")
async def create_column(column: dict):
    db = SessionLocal()

    new_column = Column(
        name=column["name"],
        board_id=column["board_id"]
    )

    db.add(new_column)
    db.commit()
    db.refresh(new_column)

    return new_column


@router.get("/columns/{board_id}")
async def get_columns(board_id: int):
    db = SessionLocal()
    columns = db.query(Column).filter(Column.board_id == board_id).all()
    return columns


# =========================
# TASKS
# =========================

@router.post("/tasks")
async def create_task(task: dict):
    db = SessionLocal()

    # ✅ Check column exists
    column = db.query(Column).filter(Column.id == task["column_id"]).first()
    if not column:
        raise HTTPException(status_code=404, detail="Column not found")

    new_task = Task(
        title=task["title"],
        description=task.get("description"),
        column_id=task["column_id"]
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    # 🔥 Real-time broadcast
    await manager.broadcast(f"Task Created: {new_task.title}")

    return new_task

@router.get("/tasks")
async def get_all_tasks():
    db = SessionLocal()
    tasks = db.query(Task).all()
    return tasks


@router.get("/tasks")
def get_all_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()


@router.put("/tasks/{task_id}")
async def update_task(task_id: int, task: dict):
    db = SessionLocal()

    existing_task = db.query(Task).filter(Task.id == task_id).first()
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")

    # ✅ Update fields
    existing_task.title = task.get("title", existing_task.title)
    existing_task.description = task.get("description", existing_task.description)
    existing_task.column_id = task.get("column_id", existing_task.column_id)

    db.commit()
    db.refresh(existing_task)

    # 🔥 Real-time broadcast
    await manager.broadcast(f"Task Updated: {existing_task.title}")

    return existing_task


@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    db = SessionLocal()

    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    # 🔥 Real-time broadcast
    await manager.broadcast(f"Task Deleted: {task.title}")

    return {"message": "Task deleted successfully"}