from typing import Dict, Any

class EmbeddingInputBuilder:
    @staticmethod
    def build_resume_text(normalized_resume: Dict[str, Any]) -> str:
        skills = normalized_resume.get("skills", {}).get("normalized", [])
        education = normalized_resume.get("education", {}).get("normalized", [])
        companies = normalized_resume.get("companies", {}).get("normalized", [])
        projects = normalized_resume.get("projects", {}).get("normalized", [])
        certifications = normalized_resume.get("certifications", {}).get("normalized", [])
        
        sections = []
        if skills:
            sections.append(f"Skills:\n{', '.join(skills)}")
        if education:
            sections.append(f"Education:\n{', '.join(education)}")
        if companies:
            sections.append(f"Experience:\n{', '.join(companies)}")
        if projects:
            sections.append(f"Projects:\n{', '.join(projects)}")
        if certifications:
            sections.append(f"Certifications:\n{', '.join(certifications)}")
            
        return "\n\n".join(sections).strip()

    @staticmethod
    def build_internship_text(normalized_internship: Dict[str, Any]) -> str:
        title = normalized_internship.get("title", "").strip()
        company = normalized_internship.get("company", "") or normalized_internship.get("company_name", "")
        company = str(company).strip()
        
        skills = normalized_internship.get("required_skills", "")
        if isinstance(skills, list):
            skills = ", ".join(skills)
        skills = str(skills).strip()
        
        description = normalized_internship.get("description", "").strip()
        
        sections = []
        if title:
            sections.append(f"Title:\n{title}")
        if company:
            sections.append(f"Company:\n{company}")
        if skills:
            sections.append(f"Skills:\n{skills}")
        if description:
            sections.append(f"Description:\n{description}")
            
        return "\n\n".join(sections).strip()
