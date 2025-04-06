from pydantic import BaseModel
from datetime import datetime

class DocumentCreate(BaseModel):
    filename: str
    filepath: str

class DocumentRead(BaseModel):
    id: int
    filename: str
    filepath: str
    status: str
    uploaded_at: datetime
