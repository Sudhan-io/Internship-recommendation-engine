import re
from typing import Dict, Any, List, Tuple
from resume.parser import ResumeParseResult
from normalization.canonical_dictionary import CanonicalDictionary
from normalization.skill_normalizer import SkillNormalizer
from normalization.education_normalizer import EducationNormalizer
from normalization.company_normalizer import CompanyNormalizer
from normalization.date_normalizer import DateNormalizer

class ResumeNormalizer:
    def __init__(self, canonical_dict: CanonicalDictionary):
        self.skill_normalizer = SkillNormalizer(canonical_dict)
        self.education_normalizer = EducationNormalizer(canonical_dict)
        self.company_normalizer = CompanyNormalizer(canonical_dict)
        self.date_normalizer = DateNormalizer()

    def normalize(self, parse_result: ResumeParseResult) -> Dict[str, Any]:
        raw_skills = parse_result.skills.values
        raw_education = parse_result.education.values
        
        raw_companies, raw_dates = self._extract_companies_and_dates(parse_result.experience.values)
        
        norm_skills, skill_changes = self.skill_normalizer.normalize(raw_skills)
        norm_education, ed_changes = self.education_normalizer.normalize(raw_education)
        norm_companies, comp_changes = self.company_normalizer.normalize(raw_companies)
        norm_dates, date_changes, date_success_rate = self.date_normalizer.normalize(raw_dates)
        
        # Calculate Quality Score
        total_entities = len(raw_skills) + len(raw_education) + len(raw_companies) + len(raw_dates)
        
        success_count = 0
        # 1. Skills success: matches loaded dictionary
        for s in norm_skills:
            if s.lower() in self.skill_normalizer.canonical_dict.skills:
                success_count += 1
        # 2. Education success: maps to dictionary values
        for e in norm_education:
            if e in self.education_normalizer.canonical_dict.education.values():
                success_count += 1
        # 3. Companies success: maps to dictionary values or cleared of suffixes
        for c in norm_companies:
            if c.lower() in self.company_normalizer.canonical_dict.companies or c in self.company_normalizer.canonical_dict.companies.values() or len(c) > 0:
                success_count += 1
        # 4. Dates success: successfully parsed to ISO
        success_count += int(date_success_rate * len(raw_dates))
        
        quality_score = (success_count / total_entities) if total_entities > 0 else 1.0
        
        return {
            "skills": {
                "original": raw_skills,
                "normalized": norm_skills
            },
            "education": {
                "original": raw_education,
                "normalized": norm_education
            },
            "companies": {
                "original": raw_companies,
                "normalized": norm_companies
            },
            "projects": {
                "original": parse_result.projects.values,
                "normalized": parse_result.projects.values
            },
            "certifications": {
                "original": parse_result.certifications.values,
                "normalized": parse_result.certifications.values
            },
            "dates": {
                "original": raw_dates,
                "normalized": norm_dates
            },
            "metadata": {
                "changes": {
                    "skills": skill_changes,
                    "education": ed_changes,
                    "companies": comp_changes,
                    "dates": date_changes
                },
                "quality_score": round(quality_score, 2)
            }
        }

    def _extract_companies_and_dates(self, experience_values: List[str]) -> Tuple[List[str], List[str]]:
        companies = []
        dates = []
        for val in experience_values:
            date_match = re.search(
                r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{4}\b.*?(?:\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{4}\b|present)",
                val, re.IGNORECASE
            )
            if not date_match:
                date_match = re.search(
                    r"\b\d{1,2}/\d{4}\s*-\s*(?:\d{1,2}/\d{4}|present)\b",
                    val, re.IGNORECASE
                )
            if date_match:
                dates.append(date_match.group(0))
                
            cleaned_val = val
            if date_match:
                cleaned_val = cleaned_val.replace(date_match.group(0), "")
                
            if " at " in cleaned_val.lower():
                parts = cleaned_val.lower().split(" at ")
                if len(parts) > 1:
                    company_part = parts[1].split(",")[0].split("-")[0].strip()
                    companies.append(company_part)
            elif "," in cleaned_val:
                parts = [p.strip() for p in cleaned_val.split(",")]
                found = False
                for part in parts:
                    if any(kw in part.lower() for kw in ["corp", "inc", "ltd", "pvt", "limited", "technologies", "solutions"]):
                        companies.append(part)
                        found = True
                        break
                if not found and len(parts) > 0:
                    companies.append(parts[0])
            else:
                companies.append(cleaned_val)
                
        return [c.strip() for c in companies if c.strip()], [d.strip() for d in dates if d.strip()]
