from fastapi import APIRouter, UploadFile, File
import io
from fastapi.responses import RedirectResponse
from ..utils import converter
from ..db import schemas
import pypdf
from ..db.config import BASE_DIR, UPLOAD_DIR

router = APIRouter(
    tags=["converter"]
)



@router.post("/save/",response_model=schemas.ExtractedText,status_code=200)
async def extract_text(file: UploadFile = File(...)):
    content = await file.read()
    pdf_file = io.BytesIO(content)

    extracted_text = converter.convert(pdf_file)
    text_length = len(extracted_text)
    return {
        "length": text_length,
        "text": extracted_text
    }



@router.post('/convert/{path}',status_code=200)
async def convert_pdf_to_excel(path: str):
    text = converter.get_txt_file(path)
    text = converter.cleanText(text)
    seat_no = converter.extract_student_details(text)
    print(seat_no)
    return {
        "status": "success",
        'seat_no': list(seat_no['seat_no'])
    }

    
    

@router.post('/extract/',status_code=200)
async def save_file(file: UploadFile = File(...)):
    content = await file.read()
    pdf_file = io.BytesIO(content)

    extracted_text = converter.convert(pdf_file)

    # save txt file
    print(file.filename)
    TXT_FILE_PATH = f'{UPLOAD_DIR}/txt/{file.filename.split(".")[0]}.txt'
    print(TXT_FILE_PATH)
    with open(TXT_FILE_PATH,'w') as txt_file:
        txt_file.write(extracted_text)

    return {
        "status": "success",
        "path":TXT_FILE_PATH
    }


