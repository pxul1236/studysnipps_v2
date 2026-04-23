from fastapi import FastAPI
from routers import notes

app = FastAPI(title="StudySnipps")

app.include_router(notes.router)

@app.get("/")
def root():
    return {"message": "StudySnipps API is live"}