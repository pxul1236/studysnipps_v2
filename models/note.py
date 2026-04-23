from sqlmodel import SQLModel

class NoteBase(SQLModel):
    title: str
    subject: str
    university: str
    file_url: str

class NoteCreate(NoteBase):
    pass

class NoteRead(NoteBase):
    id: int