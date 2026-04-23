from fastapi import APIRouter, UploadFile, File, Form
from core.database import supabase
import uuid

router = APIRouter(prefix="/notes", tags=["notes"])

@router.post("/")
async def create_note(
    title: str = Form(...),
    subject: str = Form(...),
    university: str = Form(...),
    file: UploadFile = File(...)
):
    if not file.filename.endswith(".pdf"):
        return {"error": "Only PDF files allowed"}
    
    file_bytes = await file.read()
    filename = f"{uuid.uuid4()}.pdf"
    
    supabase.storage.from_("notes").upload(
        path=filename,
        file=file_bytes,
        file_options={"content-type": "application/pdf"}
    )
    
    file_url = supabase.storage.from_("notes").get_public_url(filename)
    
    response = supabase.table("notes").insert({
        "title": title,
        "subject": subject,
        "university": university,
        "file_url": file_url
    }).execute()
    
    return response.data