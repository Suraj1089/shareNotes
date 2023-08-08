from fastapi import FastAPI, UploadFile, File
import io
import pypdf
from fastapi.responses import RedirectResponse

app = FastAPI(
    title="PDF Converter",
    description="Convert PDF to text base URL = https://converter-sharenoteservices.onrender.com",
    version="1.0.0",
    openapi_url="/converter/api/v1/auth/openapi.json",
    docs_url="/converter/api/v1/docs/",
    redoc_url="/converter/api/v1/redoc/"
)


def convert(path):
    text = ""
    reader = pypdf.PdfReader(path)
    noOfPages = len(reader.pages)
    for line in range(0,noOfPages):
        page = reader.pages[line]
        text += page.extract_text()
    return text


@app.post("/extract/")
async def extract_text(file: UploadFile = File(...)):
    content = await file.read()
    pdf_file = io.BytesIO(content)
    extracted_text = convert(pdf_file)
    text_length = len(extracted_text)
    return {
        "text": extracted_text,
        "text_length": text_length
    }


@app.get('/',include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url='/converter/api/v1/docs')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('src.main:app', host="0.0.0.0", port=8000,reload=True)
