from pydantic import BaseModel

# BOARD
class BoardCreate(BaseModel):
    name: str
    workspace_id: int

class BoardResponse(BaseModel):
    id: int
    name: str
    workspace_id: int

    class Config:
        from_attributes = True


# COLUMN
class ColumnCreate(BaseModel):
    name: str
    board_id: int

class ColumnResponse(BaseModel):
    id: int
    name: str
    board_id: int

    class Config:
        from_attributes = True


# TASK
class TaskCreate(BaseModel):
    title: str
    description: str
    column_id: int

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    column_id: int

    class Config:
        from_attributes = True