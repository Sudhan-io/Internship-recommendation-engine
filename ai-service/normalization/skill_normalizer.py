from typing import List, Tuple
from normalization.canonical_dictionary import CanonicalDictionary

class SkillNormalizer:
    def __init__(self, canonical_dict: CanonicalDictionary):
        self.canonical_dict = canonical_dict

    def normalize(self, skills: List[str]) -> Tuple[List[str], int]:
        normalized_set = set()
        change_count = 0
        
        for skill in skills:
            canonical = self.canonical_dict.get_canonical_skill(skill)
            if canonical != skill:
                change_count += 1
            normalized_set.add(canonical)
            
        return sorted(list(normalized_set)), change_count
