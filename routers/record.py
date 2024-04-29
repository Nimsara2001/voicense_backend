from fastapi import APIRouter

router = APIRouter(
    prefix="/record",
)


@router.post("/upload")
async def upload_record():
    return {"message": "Upload record"}