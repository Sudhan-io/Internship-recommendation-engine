import re
from typing import List, Tuple
from normalization.canonical_dictionary import CanonicalDictionary

class EducationNormalizer:
    def __init__(self, canonical_dict: CanonicalDictionary):
        self.canonical_dict = canonical_dict

    def normalize(self, education_entries: List[str]) -> Tuple[List[str], int]:
        normalized_set = set()
        change_count = 0
        
        for entry in education_entries:
            canonical = self.canonical_dict.get_canonical_education(entry)
            if canonical != entry:
                change_count += 1
                normalized_set.add(canonical)
            else:
                normalized_set.add(entry)
                
        return sorted(list(normalized_set)), change_count
