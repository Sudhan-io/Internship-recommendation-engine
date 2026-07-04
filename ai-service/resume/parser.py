import spacy
from typing import Dict, List
from dataclasses import dataclass, field

from nlp.section_detector import SectionDetector
from nlp.skill_extractor import SkillExtractor
from nlp.education_extractor import EducationExtractor
from nlp.experience_extractor import ExperienceExtractor
from nlp.project_extractor import ProjectExtractor
from nlp.certification_extractor import CertificationExtractor
from nlp.repository import SkillsRepository

@dataclass
class SectionResult:
    values: List[str] = field(default_factory=list)
    confidence: float = 0.0

@dataclass
class ResumeParseResult:
    skills: SectionResult = field(default_factory=SectionResult)
    education: SectionResult = field(default_factory=SectionResult)
    experience: SectionResult = field(default_factory=SectionResult)
    projects: SectionResult = field(default_factory=SectionResult)
    certifications: SectionResult = field(default_factory=SectionResult)

class ResumeParser:
    def __init__(self, skills_repository: SkillsRepository):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            # Fallback if model isn't downloaded yet
            self.nlp = None
            
        self.section_detector = SectionDetector()
        self.skill_extractor = SkillExtractor(skills_repository, self.nlp)
        self.education_extractor = EducationExtractor(self.nlp)
        self.experience_extractor = ExperienceExtractor(self.nlp)
        self.project_extractor = ProjectExtractor(self.nlp)
        self.certification_extractor = CertificationExtractor(self.nlp)

    def parse(self, text: str) -> ResumeParseResult:
        # Stage 1: Section Detection
        sections = self.section_detector.detect_sections(text)
        
        # Stage 2: Entity Extraction per Section (with general text fallback if section missing)
        
        # 1. Skills
        skills_text, skills_conf = sections["skills"]
        if not skills_text:
            skills_values = self.skill_extractor.extract(text)
            skills_conf = 0.5 if len(skills_values) > 0 else 0.0
        else:
            skills_values = self.skill_extractor.extract(skills_text)
            
        # 2. Education
        ed_text, ed_conf = sections["education"]
        if not ed_text:
            ed_values = self.education_extractor.extract(text)
            ed_conf = 0.4 if len(ed_values) > 0 else 0.0
        else:
            ed_values = self.education_extractor.extract(ed_text)
            
        # 3. Experience
        exp_text, exp_conf = sections["experience"]
        if not exp_text:
            exp_values = self.experience_extractor.extract(text)
            exp_conf = 0.4 if len(exp_values) > 0 else 0.0
        else:
            exp_values = self.experience_extractor.extract(exp_text)
            
        # 4. Projects
        proj_text, proj_conf = sections["projects"]
        if not proj_text:
            proj_values = self.project_extractor.extract(text)
            proj_conf = 0.4 if len(proj_values) > 0 else 0.0
        else:
            proj_values = self.project_extractor.extract(proj_text)
            
        # 5. Certifications
        cert_text, cert_conf = sections["certifications"]
        if not cert_text:
            cert_values = self.certification_extractor.extract(text)
            cert_conf = 0.4 if len(cert_values) > 0 else 0.0
        else:
            cert_values = self.certification_extractor.extract(cert_text)
            
        return ResumeParseResult(
            skills=SectionResult(values=skills_values, confidence=skills_conf),
            education=SectionResult(values=ed_values, confidence=ed_conf),
            experience=SectionResult(values=exp_values, confidence=exp_conf),
            projects=SectionResult(values=proj_values, confidence=proj_conf),
            certifications=SectionResult(values=cert_values, confidence=cert_conf)
        )
