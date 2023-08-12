from pydantic import BaseModel


class ExtractedText(BaseModel):
    text: str
    text_length: int

    class Config:
        schema_extra = {
            "example": {
                "text": "This is the text extracted from the pdf file",
                "text_length": 45
            }
        }