from fastapi import APIRouter
from schemas.resume import ResumeParseRequest, ResumeParseResponse, SectionResponse
from nlp.repository import SkillsRepository
from resume.parser import ResumeParser, ResumeParseResult

router = APIRouter(prefix="/resume", tags=["Resume"])

# Load repository and parser
skills_repo = SkillsRepository()
parser = ResumeParser(skills_repo)

def map_to_response(result: ResumeParseResult) -> ResumeParseResponse:
    return ResumeParseResponse(
        skills=SectionResponse(values=result.skills.values, confidence=result.skills.confidence),
        education=SectionResponse(values=result.education.values, confidence=result.education.confidence),
        experience=SectionResponse(values=result.experience.values, confidence=result.experience.confidence),
        projects=SectionResponse(values=result.projects.values, confidence=result.projects.confidence),
        certifications=SectionResponse(values=result.certifications.values, confidence=result.certifications.confidence)
    )

@router.post("/parse", response_model=ResumeParseResponse)
def parse_resume(request: ResumeParseRequest):
    result = parser.parse(request.text)
    return map_to_response(result)
