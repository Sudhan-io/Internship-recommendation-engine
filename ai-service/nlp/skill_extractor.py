import re
import spacy
from typing import List
from nlp.repository import SkillsRepository

class SkillExtractor:
    def __init__(self, repository: SkillsRepository, nlp=None):
        self.repository = repository
        self.nlp = nlp if nlp else spacy.load("en_core_web_sm")
        self.skills_list = self.repository.get_all_skills()

    def extract(self, text: str) -> List[str]:
        if not text:
            return []
        
        extracted = []
        for skill in self.skills_list:
            escaped_skill = re.escape(skill)
            # Custom word boundary handling for tech keywords like C++, C#, .NET, Node.js
            if skill.endswith("+") or skill.endswith("#") or "." in skill or "-" in skill:
                pattern = rf"(?i)(?:^|\s|/|,|;){escaped_skill}(?:$|\s|/|,|;|\.)"
            else:
                pattern = rf"(?i)\b{escaped_skill}\b"
                
            if re.search(pattern, text):
                extracted.append(skill)
        return sorted(list(set(extracted)))
