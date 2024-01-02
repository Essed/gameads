from importlib.resources import path
from api.__init__ import *
from api.actions.upload import _upload_file
from fastapi import File, UploadFile
from fastapi.responses import FileResponse

from db.models import User

upload_router = APIRouter()


@upload_router.post("/", response_model=UploadedFileResonse)
async def upload_file(upload_file: UploadFile = File(...)) -> UploadedFileResonse:
    
    path = await _upload_file(upload_file)

    return UploadedFileResonse(img_url=path)



@upload_router.get("/{file_name}", response_class=FileResponse)
async def download_file(file_name: str):
    path = f"img/{file_name}"
    return path