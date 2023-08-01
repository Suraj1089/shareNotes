from fastapi import FastAPI, UploadFile, File
import io
import PyPDF2

app = FastAPI()

def extract_text_from_pdf(pdf_file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text.strip()

# reader = PdfReader("example.pdf")
# number_of_pages = len(reader.pages)
# page = reader.pages[0]
# text = page.extract_text()
import pypdf
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host="0.0.0.0", port=8000,reload=True)
