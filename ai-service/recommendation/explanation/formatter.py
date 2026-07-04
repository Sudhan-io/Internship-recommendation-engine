from typing import List

class ExplanationFormatter:
    @staticmethod
    def format_explanation(
        overall_score: float,
        matched_skills: List[str],
        missing_skills: List[str],
        matched_education: List[str],
        eligibility_status: bool
    ) -> str:
        parts = [f"This internship has an overall score of {overall_score * 100:.1f}%."]
        
        if matched_skills:
            parts.append(f"Matched skills: {', '.join(matched_skills)}.")
        if missing_skills:
            parts.append(f"Missing skills: {', '.join(missing_skills)}.")
            
        if matched_education:
            parts.append(f"Your education ({', '.join(matched_education)}) matches the requirements.")
        else:
            parts.append("No education matches found or required.")
            
        status_str = "meets" if eligibility_status else "does not meet"
        parts.append(f"Your profile {status_str} the location and work mode eligibility criteria.")
        
        return " ".join(parts)
