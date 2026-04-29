from fastapi import HTTPException
from app.models.workspace import Workspace
from app.models.workspace_member import WorkspaceMember

def check_workspace_access(db, workspace_id, user_id):
    workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()

    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")

    if workspace.owner_id == user_id:
        return True

    member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == workspace_id,
        WorkspaceMember.user_id == user_id
    ).first()

    if not member:
        raise HTTPException(status_code=403, detail="Access denied")

    return True