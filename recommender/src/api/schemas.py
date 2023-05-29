from pydantic import BaseModel




class Recoomendation(BaseModel):
    expertise: str
    skills: list[str]