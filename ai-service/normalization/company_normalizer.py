import re
from typing import List, Tuple
from normalization.canonical_dictionary import CanonicalDictionary

class CompanyNormalizer:
    def __init__(self, canonical_dict: CanonicalDictionary):
        self.canonical_dict = canonical_dict
        self.suffix_pattern = re.compile(
            r"\b(inc\.|inc|llc|corp\.|corp|corporation|pvt\s+ltd|ltd\.|ltd|co\.|co)\b",
            re.IGNORECASE
        )

    def normalize(self, companies: List[str]) -> Tuple[List[str], int]:
        normalized_list = []
        change_count = 0
        
        for company in companies:
            # Suffix removal
            cleaned = self.suffix_pattern.sub("", company).strip()
            cleaned = re.sub(r"[\s,.-]+$", "", cleaned).strip()
            
            # Lookup in canonical dictionary
            canonical = self.canonical_dict.get_canonical_company(cleaned)
            
            if canonical == cleaned:
                canonical = cleaned.title()
                
            if canonical != company:
                change_count += 1
                
            if canonical:
                normalized_list.append(canonical)
                
        return sorted(list(set(normalized_list))), change_count
