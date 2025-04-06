from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.db.database import get_session
from app.models.document_model import Document
import shutil
import os

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_document(file: UploadFile = File(...), session: AsyncSession = Depends(get_session), background_tasks: BackgroundTasks = None):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    document = Document(filename=file.filename, filepath=file_location)
    session.add(document)
    session.commit()
    session.refresh(document)
    
    # Simulate background processing
    background_tasks.add_task(simulate_processing, document.id, session)
    
    return {"id": document.id, "filename": document.filename}

@router.get("/documents")
async def list_documents(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Document))
    documents = result.scalars().all()
    return documents

@router.get("/documents/{document_id}")
async def get_document(document_id: int, session: AsyncSession = Depends(get_session)):
    document = await session.get(Document, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document

def simulate_processing(document_id: int, session: AsyncSession):
    import time
    time.sleep(2)  # simulate long task
    
    document = session.get(Document, document_id)
    if document:
        document.status = "processed"
        session.add(document)
        session.commit()
