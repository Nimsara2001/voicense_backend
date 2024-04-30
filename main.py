from fastapi import FastAPI

from db_config import get_db
from routers import note, auth, module, record
import uvicorn

app = FastAPI()

app.include_router(auth.router)
app.include_router(note.router)
app.include_router(module.router)
app.include_router(record.router)


@app.get("/")
async def root():
    db = get_db()
    return {"message": db.list_collection_names()}


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
