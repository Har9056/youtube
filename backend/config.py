### backend/config.py

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
    PGUSER = os.getenv("PGUSER")
    PGPASSWORD = os.getenv("PGPASSWORD")
    PGHOST = os.getenv("PGHOST")
    PGDATABASE = os.getenv("PGDATABASE")
    PGSSLMODE = os.getenv("PGSSLMODE", "require")

    @classmethod
    def get_database_url(cls):
        return f"postgresql://{cls.PGUSER}:{cls.PGPASSWORD}@{cls.PGHOST}/{cls.PGDATABASE}?sslmode={cls.PGSSLMODE}"

    DATABASE_URL = property(lambda cls: cls.get_database_url())