from fastapi import File, UploadFile
from fastapi.responses import FileResponse

import shutil
import uuid

async def _upload_file(upload_file: UploadFile = File(...)):
     
    unique_id = str(uuid.uuid4())
    file_extention = upload_file.filename.split(".")[-1]
    upload_file.filename = f"{unique_id}.{file_extention}"
    print(upload_file)
    path = f"img/{upload_file.filename}" 

    with open(path, "wb+") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    return path