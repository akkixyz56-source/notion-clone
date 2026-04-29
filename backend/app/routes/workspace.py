from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.workspace import Workspace
from app.models.user import User
from app.models.workspace_member import WorkspaceMember
from app.core.deps import get_current_user

router = APIRouter()


# ✅ CREATE WORKSPACE
@router.post("/workspace/")
def create_workspace(
    name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    workspace = Workspace(
        name=name,
        owner_id=current_user.id
    )

    db.add(workspace)
    db.commit()
    db.refresh(workspace)

    # add owner as member
    member = WorkspaceMember(
        user_id=current_user.id,
        workspace_id=workspace.id,
        role="owner"
    )

    db.add(member)
    db.commit()

    return {
        "message": "Workspace created",
        "workspace_id": workspace.id
    }


# ✅ INVITE USER
@router.post("/workspace/{workspace_id}/invite")
def invite_user(
    workspace_id: int,
    email: str,
    role: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()

    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")

    # 🔍 DEBUG (optional)
    print("Current user:", current_user.id)
    print("Workspace owner:", workspace.owner_id)

    # ✅ ONLY OWNER CAN INVITE
    if workspace.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only owner can invite")

    # find user to invite
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # check already member
    existing = db.query(WorkspaceMember).filter(
        WorkspaceMember.user_id == user.id,
        WorkspaceMember.workspace_id == workspace_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="User already a member")

    # add member
    member = WorkspaceMember(
        user_id=user.id,
        workspace_id=workspace_id,
        role=role
    )

    db.add(member)
    db.commit()

    return {"message": "User invited successfully"}


# ✅ GET ALL WORKSPACES (for current user)
@router.get("/workspace/")
def get_workspaces(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    memberships = db.query(WorkspaceMember).filter(
        WorkspaceMember.user_id == current_user.id
    ).all()

    workspaces = []
    for m in memberships:
        workspace = db.query(Workspace).filter(
            Workspace.id == m.workspace_id
        ).first()

        workspaces.append({
            "id": workspace.id,
            "name": workspace.name,
            "role": m.role
        })

    return workspaces