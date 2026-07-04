import re
from typing import List, Tuple

class DateNormalizer:
    def __init__(self):
        self.months_map = {
            "jan": "01", "january": "01",
            "feb": "02", "february": "02",
            "mar": "03", "march": "03",
            "apr": "04", "april": "04",
            "may": "05",
            "jun": "06", "june": "06",
            "jul": "07", "july": "07",
            "aug": "08", "august": "08",
            "sep": "09", "september": "09",
            "oct": "10", "october": "10",
            "nov": "11", "november": "11",
            "dec": "12", "december": "12"
        }
        self.month_year_pattern = re.compile(
            r"\b(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\b\s*,?\s*\b(\d{4})\b",
            re.IGNORECASE
        )
        self.numeric_pattern = re.compile(
            r"\b(0?[1-9]|1[0-2])\s*[\/-]\s*(\d{4})\b"
        )

    def normalize_single_string(self, text: str) -> Tuple[str, bool]:
        cleaned = text.strip()
        
        match1 = self.month_year_pattern.search(cleaned)
        if match1:
            month_str = match1.group(1).lower()
            year_str = match1.group(2)
            month_num = self.months_map.get(month_str, "01")
            return f"{year_str}-{month_num}", True
            
        match2 = self.numeric_pattern.search(cleaned)
        if match2:
            month_str = match2.group(1).zfill(2)
            year_str = match2.group(2)
            return f"{year_str}-{month_str}", True
            
        if "present" in cleaned.lower():
            return "Present", True
            
        return text, False

    def normalize(self, date_strings: List[str]) -> Tuple[List[str], int, float]:
        normalized_list = []
        change_count = 0
        success_count = 0
        total_parts = 0
        
        for date_str in date_strings:
            parts = re.split(r'\s+to\s+|\s*-\s*|\s*–\s*|\s+until\s+', date_str, flags=re.IGNORECASE)
            normalized_parts = []
            
            for part in parts:
                total_parts += 1
                norm, success = self.normalize_single_string(part)
                normalized_parts.append(norm)
                if success:
                    success_count += 1
                       
            normalized_combined = " - ".join(normalized_parts)
            if normalized_combined != date_str:
                change_count += 1
                   
            normalized_list.append(normalized_combined)
               
        success_rate = (success_count / total_parts) if total_parts > 0 else 1.0
        
        return normalized_list, change_count, success_rate
