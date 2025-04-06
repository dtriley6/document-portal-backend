from sqlmodel import SQLModel, Field
from datetime import datetime

class Document(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    filename: str
    filepath: str
    status: str = "uploaded"
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
