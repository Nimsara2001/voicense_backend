from fastapi import FastAPI
from routers import note, auth, module, record

app = FastAPI()

app.include_router(auth.router)
app.include_router(note.router)
app.include_router(module.router)
app.include_router(record.router)


@app.get("/")
async def root():
    return {"message": "Server is running..."}