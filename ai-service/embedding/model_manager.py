import threading
from sentence_transformers import SentenceTransformer

class ModelManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(ModelManager, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        if self._initialized:
            return
        self.model_name = model_name
        self.model = None
        self._load_model()
        self._initialized = True

    def _load_model(self):
        try:
            self.model = SentenceTransformer(self.model_name)
            print(f"[ModelManager] Model '{self.model_name}' loaded successfully.")
        except Exception as e:
            print(f"[ModelManager] Error loading model '{self.model_name}': {e}")
            self.model = None

    def get_model(self) -> SentenceTransformer:
        if self.model is None:
            raise RuntimeError(f"SentenceTransformer model '{self.model_name}' was not successfully loaded.")
        return self.model
