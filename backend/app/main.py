from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ✅ IMPORTANT: Import models BEFORE create_all
from app.models.notification import Notification

# Database
from app.db.database import Base, engine

# Routers
from app.routes.kanban import router as kanban_router
from app.routes.notes import router as notes_router
from app.routes.analytics import router as analytics_router
from app.routes.notifications import router as notifications_router


# ✅ Create tables (AFTER importing models)
Base.metadata.create_all(bind=engine)


# Initialize FastAPI app
app = FastAPI(title="Notion Clone API")


# ✅ CORS (for React frontend)
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ✅ Include routers
app.include_router(kanban_router, prefix="/kanban")
app.include_router(notes_router, prefix="/notes", tags=["Notes"])
app.include_router(analytics_router, tags=["Analytics"])
app.include_router(notifications_router, prefix="/notifications", tags=["Notifications"])


# ✅ Root API
@app.get("/")
def root():
    return {"message": "Backend is running 🚀"}