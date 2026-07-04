import re
import spacy
from typing import List

class CertificationExtractor:
    def __init__(self, nlp=None):
        self.nlp = nlp if nlp else spacy.load("en_core_web_sm")

    def extract(self, text: str) -> List[str]:
        if not text:
            return []
        
        lines = text.splitlines()
        certification_entries = []
        
        for line in lines:
            line_str = line.strip()
            if not line_str:
                continue
            
            keywords = ["certified", "certification", "certificate", "course", "training", "license", "udemy", "coursera", "nptel", "aws", "google", "microsoft", "oracle", "credential", "academy"]
            has_keyword = any(kw in line_str.lower() for kw in keywords)
            
            if has_keyword:
                if len(line_str.split()) < 20:
                    certification_entries.append(line_str)
                    
        return certification_entries
