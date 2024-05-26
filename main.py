from fastapi import FastAPI, Depends

from controller.auth_bearer import JWTBearer
from routers import note, auth, module, record
from db_config import get_db

app = FastAPI(debug=True)

app.include_router(auth.router, tags=["Auth"])
app.include_router(note.router, tags=["Note"],dependencies=[Depends(JWTBearer())])
app.include_router(module.router, tags=["Module"],dependencies=[Depends(JWTBearer())])
app.include_router(record.router, tags=["Record"],dependencies=[Depends(JWTBearer())])


@app.get("/")
async def root():
    db = await get_db()
    return {"db collections": await db.list_collection_names()}
