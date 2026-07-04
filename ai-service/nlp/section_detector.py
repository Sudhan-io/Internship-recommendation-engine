import re
from typing import Dict, Tuple

class SectionDetector:
    def __init__(self):
        self.headings = {
            "skills": [r"\bskills\b", r"\btechnical skills\b", r"\bcore skills\b", r"\btechnologies\b", r"\bkey skills\b", r"\bexpertise\b"],
            "education": [r"\beducation\b", r"\bacademic background\b", r"\bacademic qualifications\b", r"\bacademics\b", r"\bqualification\b", r"\bacademic details\b"],
            "experience": [r"\bexperience\b", r"\bwork history\b", r"\bwork experience\b", r"\bprofessional experience\b", r"\bemployment history\b", r"\binternships\b", r"\bemployment\b"],
            "projects": [r"\bprojects\b", r"\bacademic projects\b", r"\bpersonal projects\b", r"\bkey projects\b", r"\bresearch projects\b"],
            "certifications": [r"\bcertifications\b", r"\bcertificates\b", r"\bcertification\b", r"\bcredentials\b", r"\bcourses\b", r"\btraining\b"]
        }

    def detect_sections(self, text: str) -> Dict[str, Tuple[str, float]]:
        lines = text.splitlines()
        sections_content = {
            "skills": [],
            "education": [],
            "experience": [],
            "projects": [],
            "certifications": []
        }
        
        current_section = None
        detected_sections = set()
        
        for line in lines:
            trimmed = line.strip()
            if not trimmed:
                continue
            
            # Identify if the line is a section header
            found_heading = False
            for section, patterns in self.headings.items():
                for pattern in patterns:
                    # Match heading (must be short, e.g. <= 4 words)
                    if len(trimmed.split()) <= 4 and re.search(pattern, trimmed.lower()):
                        current_section = section
                        detected_sections.add(section)
                        found_heading = True
                        break
                if found_heading:
                    break
            
            if found_heading:
                continue
            
            if current_section:
                sections_content[current_section].append(line)
        
        result = {}
        for section, lines_list in sections_content.items():
            section_text = "\n".join(lines_list).strip()
            if section in detected_sections:
                confidence = 1.0 if len(section_text) > 0 else 0.0
            else:
                confidence = 0.0
            result[section] = (section_text, confidence)
            
        return result
