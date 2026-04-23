from sqlmodel import SQLModel

class NoteBase(SQLModel):
    title: str
    subject: str
    description: str
    university: str

class NoteCreate(NoteBase):
    pass

class NoteRead(NoteBase):
    id: int