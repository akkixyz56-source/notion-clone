from sqlalchemy import Column, Integer, String
from app.db.database import Base

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, nullable=False)
    status = Column(String, default="unread")  