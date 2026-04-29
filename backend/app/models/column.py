from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.database import Base

class Column(Base):
    __tablename__ = "columns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    board_id = Column(Integer, ForeignKey("boards.id"))