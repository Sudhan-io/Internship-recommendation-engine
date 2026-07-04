from pydantic import BaseModel
from typing import List

class ResumeParseRequest(BaseModel):
    text: str

class SectionResponse(BaseModel):
    values: List[str]
    confidence: float

class ResumeParseResponse(BaseModel):
    skills: SectionResponse
    education: SectionResponse
    experience: SectionResponse
    projects: SectionResponse
    certifications: SectionResponse
