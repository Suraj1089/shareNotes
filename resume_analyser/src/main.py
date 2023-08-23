from fastapi import FastAPI, UploadFile, File
import io
import pypdf
from fastapi.responses import RedirectResponse
from .routes import converter
from .db.config import BASE_DIR

app = FastAPI(
    title="PDF Converter",
    description="Convert PDF to Excel base URL = https://converter-sharenoteservices.onrender.com",
    version="1.0.0",
    openapi_url="/converter/api/v1/auth/openapi.json",
    docs_url="/converter/api/v1/docs/",
    redoc_url="/converter/api/v1/redoc/"
)

app.include_router(converter.router)

@app.get('/',include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url='/converter/api/v1/docs')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('src.main:app', host="0.0.0.0", port=8000,reload=True)
