import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # من Hugging Face
    HF_API_TOKEN = os.getenv("HF_API_TOKEN")
    HF_MODEL_NAME = os.getenv("HF_MODEL_NAME", "microsoft/phi-2")
    
    # إعدادات عامة
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")