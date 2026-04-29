from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.database import Base

class WorkspaceMember(Base):
    __tablename__ = "workspace_members"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    workspace_id = Column(Integer, ForeignKey("workspaces.id"))
    role = Column(String)  # owner / editor / viewer