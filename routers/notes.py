from fastapi import APIRouter, UploadFile, File, Form
from core.database import supabase
import uuid
import requests
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/notes", tags=["notes"])

@router.get("/")
def get_notes():
    response = supabase.table("notes").select("*").execute()
    return response.data

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

    # Bypass supabase client storage bug, upload directly
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

    upload_url = f"{SUPABASE_URL}/storage/v1/object/notes/{filename}"
    
    headers = {
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/pdf",
        "x-upsert": "true"
    }

    upload_response = requests.post(upload_url, headers=headers, data=file_bytes)

    if upload_response.status_code != 200:
        return {"error": "File upload failed", "details": upload_response.text}

    # Build public URL manually
    file_url = f"{SUPABASE_URL}/storage/v1/object/public/notes/{filename}"

    response = supabase.table("notes").insert({
        "title": title,
        "subject": subject,
        "university": university,
        "file_url": file_url
    }).execute()

    return response.data