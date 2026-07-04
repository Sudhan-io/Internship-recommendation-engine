import re
import spacy
from typing import List

class ProjectExtractor:
    def __init__(self, nlp=None):
        self.nlp = nlp if nlp else spacy.load("en_core_web_sm")

    def extract(self, text: str) -> List[str]:
        if not text:
            return []
        
        lines = text.splitlines()
        projects_entries = []
        
        for line in lines:
            line_str = line.strip()
            if not line_str:
                continue
            
            word_count = len(line_str.split())
            if word_count > 0:
                is_capitalized = line_str[0].isupper()
                has_tech_indicator = any(kw in line_str.lower() for kw in ["using", "built with", "developed", "stack", "project", "system", "app", "application", "website", "model", "github"])
                
                if (word_count <= 8 and is_capitalized) or has_tech_indicator:
                    if word_count < 25:
                        projects_entries.append(line_str)
                        
        return projects_entries
