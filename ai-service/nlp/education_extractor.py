import re
import spacy
from typing import List

class EducationExtractor:
    def __init__(self, nlp=None):
        self.nlp = nlp if nlp else spacy.load("en_core_web_sm")
        self.degree_keywords = [
            r"\bB\.?E\b", r"\bB\.?Tech\b", r"\bM\.?Tech\b", r"\bB\.?S\b", r"\bM\.?S\b",
            r"\bB\.?Sc\b", r"\bM\.?Sc\b", r"\bM\.?C\.?A\b", r"\bM\.?B\.?A\b",
            r"\bBachelor(?:'s)?\b", r"\bMaster(?:'s)?\b", r"\bPh\.?D\b"
        ]

    def extract(self, text: str) -> List[str]:
        if not text:
            return []
        
        lines = text.splitlines()
        education_entries = []
        
        for line in lines:
            line_str = line.strip()
            if not line_str:
                continue
            
            has_degree = any(re.search(pat, line_str, re.IGNORECASE) for pat in self.degree_keywords)
            has_college = any(kw in line_str.lower() for kw in ["university", "college", "institute", "school", "academy", "iit", "nit", "vidyalaya"])
            has_gpa = any(kw in line_str.lower() for kw in ["gpa", "cgpa", "percentage", "g.p.a", "c.g.p.a"]) or re.search(r"\b\d\.\d{1,2}(?:\s*/\s*10)?\b", line_str)
            
            if has_degree or has_college or has_gpa:
                education_entries.append(line_str)
                
        return education_entries
