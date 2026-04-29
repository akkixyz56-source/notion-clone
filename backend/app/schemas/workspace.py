from pydantic import BaseModel

class WorkspaceCreate(BaseModel):
    name: str

class InviteUser(BaseModel):
    email: str
    role: str