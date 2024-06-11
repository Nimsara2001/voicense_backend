import asyncio
from fastapi import FastAPI, Depends, BackgroundTasks

from controller.auth_bearer import JWTBearer
from routers import note, auth, module, record
from db_config import get_db

app = FastAPI(debug=True)

app.include_router(auth.router, tags=["Auth"])
app.include_router(note.router, tags=["Note"],dependencies=[Depends(JWTBearer())])
app.include_router(module.router, tags=["Module"],dependencies=[Depends(JWTBearer())])
app.include_router(record.router, tags=["Record"],dependencies=[Depends(JWTBearer())])

# app.include_router(note.router, tags=["Note"])
# app.include_router(module.router, tags=["Module"])
# app.include_router(record.router, tags=["Record"])


@app.get("/")
async def root():
    db = await get_db()
    return {"db collections": await db.list_collection_names()}


async def write_notification(email: str, message=""):
    content = f"notification for {email}: {message}"
    await asyncio.sleep(20)
    return content


@app.get("/test")
async def test(background_tasks: BackgroundTasks, email: str):
    background_tasks.add_task(write_notification, email, message="some notification")
    return "Test notification sent in the background"
