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
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)
