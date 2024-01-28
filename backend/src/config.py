import os

from dotenv import load_dotenv
from loguru import logger
from pydantic import BaseModel, Field


def redact(name: str, value: str) -> str:
    # if ends with _KEY, redact
    if name.endswith("_KEY"):
        return "[REDACTED]"
    else:
        return value


class GlobalConfig(BaseModel):
    cooldown_global: int = Field(default=30)
    cooldown_individual: int = Field(default=5)
    tts: bool = Field(default=True)

    elevenlabs_buffer_size: int = Field(default=2048)
    chatgpt_buffer_size: int = Field(default=10)

    openai_streaming: bool = Field(default=True)
    openai_api_key: str = Field(default="")
    openai_base_url: str = Field(default="https://api.openai.com/v1")
    openai_model: str = Field(default="gpt-4-turbo-preview")

    elevenlabs_streaming: bool = Field(default=True)
    elevenlabs_api_key: str = Field(default="")
    elevenlabs_voice_id: str = Field(default="")

    narrator_volume: int = Field(default=100)

    @classmethod
    def from_env(cls):
        load_dotenv(".env", override=True)
        logger.debug("Loading config from .env")
        c = cls(**{f: os.getenv(f.upper()) for f in cls.model_fields})  # type: ignore
        logger.debug(f"Loaded config: {c}")
        return c

    def save(self):
        logger.debug("Saving config to .env")
        with open(".env", "w") as f:
            attributes = [f for f in self.model_fields]
            for attribute in attributes:
                value = getattr(self, attribute, None)
                if value is not None:
                    f.write(f"{attribute.upper()}={value}\n")
        logger.info("Saved config to .env")

    def update(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.save()


if os.path.isfile(".env"):
    logger.debug("Loading config from .env")
    global_config = GlobalConfig.from_env()
else:
    logger.debug("No .env file found, creating one")
    global_config = GlobalConfig()
    global_config.save()
