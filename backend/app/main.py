from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.db.database import Base, engine
from app.routes import auth, workspace, note, kanban, ws
from app.models.user import User

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(workspace.router)
app.include_router(note.router)
app.include_router(kanban.router, prefix="/kanban", tags=["Kanban"])
app.include_router(ws.router, prefix="/ws")



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)