from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.db.database import get_session, async_session
from app.models.document_model import Document
import shutil
import os


router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
):
    # Save file to disk
    upload_folder = "uploads"
    os.makedirs(upload_folder, exist_ok=True)
    file_location = f"{upload_folder}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Save record to DB
    document = Document(filename=file.filename, filepath=file_location)

    session.add(document)
    await session.commit()          # Important: Commit first
    await session.refresh(document) # Then refresh to get real ID

    background_tasks.add_task(simulate_processing, document.id)

    return {
        "id": document.id,
        "filename": document.filename,
        "status": document.status,
        "uploaded_at": document.uploaded_at,
    }


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

async def simulate_processing(document_id: int):
    async with async_session() as session:
        document = await session.get(Document, document_id)
        if document:
            document.status = "processed"
            await session.commit()