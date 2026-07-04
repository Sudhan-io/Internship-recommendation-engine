from abc import ABC, abstractmethod
from typing import Dict, Any

class Scorer(ABC):
    @property
    @abstractmethod
    def weight(self) -> float:
        pass

    @abstractmethod
    def calculate_score(self, resume: Dict[str, Any], internship: Dict[str, Any], similarity_score: float) -> float:
        pass
