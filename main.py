from fastapi import FastAPI
from routers import note, auth, module, record
import uvicorn

app = FastAPI()

app.include_router(auth.router)
app.include_router(note.router)
app.include_router(module.router)
app.include_router(record.router)


@app.get("/")
async def root():
    return {"message": "Server is running..."}


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)


# User
#    -userId
#    -userType
#    -firstName
#    -lastName
#    -username
#    -password
#
# transcription
#    -transcriptionId
#    -content
#    -generatedDate
#
# lectureNote
#    -noteId
#    -topic
#    -noteViewText (for note view card)
#    -content (as a markdown format)
#    -createdDate
#    -lastAccessDate
#    -transcriptionId
#    -moduleId
#
# Module
#    -moduleId
#    -title
#    -createdDate
#
# Prompt
#    -promptId
#    -prompt