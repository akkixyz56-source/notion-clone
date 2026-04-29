from pydantic import BaseModel

class NoteCreate(BaseModel):
    workspace_id: int
    content: str


class NoteUpdate(BaseModel):
    content: str


class NoteResponse(BaseModel):
    id: int
    content: str
    workspace_id: int

    class Config:
        from_attributes = True