from fastapi import APIRouter, UploadFile, File
import io
from fastapi.responses import RedirectResponse
from ..utils import converter
from ..db import schemas
import pypdf
from ..db.config import BASE_DIR
import shutil
from fastapi import status
from fastapi.responses import JSONResponse
import os 


router = APIRouter(
    tags=["converter"]
)


# route to upload user uploaded resume files
@router.post("/upload",status_code=status.HTTP_201_CREATED)
def upload(file: UploadFile = File(...)):
    try:
        # if folder not present
        path = BASE_DIR / 'uploads/pdf'
        if not os.path.exists(path=path):
            os.makedirs(path)
        
        with open(f'{path}/{file.filename}', 'wb') as f:
            shutil.copyfileobj(file.file, f)
    
    except Exception as e:
        return JSONResponse(
            content=f'Error in uploading {file.filename}',
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    finally:
        file.file.close()
        
    return {"message": f"Successfully uploaded {file.filename}",
            "path": BASE_DIR / f'uploads/pdf/{file.filename}'
            }


@router.post('/analyse')
def analyse_resume(path: str):
    pass 