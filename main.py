from fastapi import FastAPI
from db_config import get_db
from routers import note, auth, module, record
import uvicorn

app = FastAPI()

app.include_router(auth.router, tags=["Auth"])
app.include_router(note.router, tags=["Note"])
app.include_router(module.router, tags=["Module"])
app.include_router(record.router, tags=["Record"])


@app.get("/")
async def root():
    db = get_db()
    return {"message": db.list_collection_names()}


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
