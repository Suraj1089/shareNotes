from fastapi import FastAPI, UploadFile, File
import io
import pypdf
from fastapi.responses import RedirectResponse
from .routes import converter
from .db.config import BASE_DIR

app = FastAPI(
    title="PDF Converter",
)

app.include_router(converter.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run('src.main:app', host="0.0.0.0", port=8000,reload=True)
