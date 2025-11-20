from fastapi import APIRouter, UploadFile, File, HTTPException
import uuid
from services.spaces import upload_file_to_space 

picture_router = APIRouter()

@picture_router.post("/upload/photo/")
async def upload_photo(
    photo: UploadFile = File(...)
):
    file_extension = photo.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    
    file_url = upload_file_to_space(
        file=photo,
        object_name=unique_filename,
        content_type=photo.content_type
    )

    if file_url:
        return {"status_code": 200, "url": file_url}
    else:
        raise HTTPException(status_code=500, detail="Fallo al subir el archivo a DigitalOcean Spaces.")

