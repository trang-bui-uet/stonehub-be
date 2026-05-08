from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        enable_decoding=False,
    )
    gemini_api_key: str = Field(alias="GEMINI_API_KEY")
    gemini_model: str = Field(default="gemini-2.5-flash", alias="GEMINI_MODEL")
    cors_origins: List[str] = Field(default=["http://localhost:5173"], alias="CORS_ORIGINS")
    cors_origin_regex: str = Field(
        default=r"https://.*\.(ngrok-free\.dev|trycloudflare\.com)",
        alias="CORS_ORIGIN_REGEX",
    )

    @field_validator("cors_origins", mode="before")
    @classmethod
    def validate_cors_origins(cls, input_value: str | List[str]) -> List[str]:
        if isinstance(input_value, list):
            return input_value
        if isinstance(input_value, str):
            return [origin.strip() for origin in input_value.split(",") if origin.strip()]
        return ["http://localhost:5173"]


settings = Settings()
