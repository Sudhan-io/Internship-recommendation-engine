import re
import spacy
from typing import List

class ExperienceExtractor:
    def __init__(self, nlp=None):
        self.nlp = nlp if nlp else spacy.load("en_core_web_sm")
        self.role_keywords = [
            r"\bdeveloper\b", r"\bengineer\b", r"\bintern\b", r"\banalyst\b",
            r"\bmanager\b", r"\blead\b", r"\bconsultant\b", r"\bprogrammer\b",
            r"\barchitect\b", r"\bspecialist\b", r"\badministrator\b"
        ]

    def extract(self, text: str) -> List[str]:
        if not text:
            return []
        
        lines = text.splitlines()
        experience_entries = []
        
        for line in lines:
            line_str = line.strip()
            if not line_str:
                continue
            
            has_role = any(re.search(pat, line_str, re.IGNORECASE) for pat in self.role_keywords)
            has_date_range = re.search(r"\b\d{4}\b|\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{4}\b", line_str, re.IGNORECASE) is not None
            has_company = any(kw in line_str.lower() for kw in ["pvt", "ltd", "corp", "inc", "technologies", "solutions", "limited", "systems", "corporation"]) or " at " in line_str.lower()
            
            if has_role or (has_date_range and len(line_str.split()) > 3) or has_company:
                if len(line_str.split()) < 25:
                    experience_entries.append(line_str)
                    
        return experience_entries
