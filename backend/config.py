from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "LegalEase"
    company_name: str = "LegalEase"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    demo_mode: bool = False
    backend_url: str = "http://127.0.0.1:8000"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def ai_enabled(self) -> bool:
        return bool(self.gemini_api_key.strip()) and not self.demo_mode


@lru_cache
def get_settings() -> Settings:
    return Settings()
