from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.database import Base

class Board(Base):
    __tablename__ = "boards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"))