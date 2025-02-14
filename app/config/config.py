import os.path

from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings

__all__ = ["Symbols", "PGSettings", "BinanceSettings", "TGBotSettings", "RedisSettings"]


class Settings(BaseSettings):
    class Config:
        env_file = os.path.abspath(os.path.join('.env'))
        extra = "ignore"


class Symbols(Settings):
    SYMBOLS: str


class PGSettings(Settings):
    USER: str
    PASSWORD: SecretStr
    DB_NAME: str
    HOST: str
    PORT: int
    POOL_SIZE: int
    MAX_OVERFLOW: int
    ECHO: bool

    class Config:
        env_prefix = "POSTGRES_"


class RedisSettings(Settings):
    HOST: str
    PORT: int
    MAX_CONNECTIONS: int
    TIMEOUT: int

    class Config:
        env_prefix = "REDIS_"


class TGBotSettings(Settings):
    TOKEN: SecretStr

    class Config:
        env_prefix = "BOT_"


class BinanceSettings(Settings):
    """
    Конфиг для биржи Binance. Обязателен для каждой новой биржи.
    Названия классов конфигов по схеме: название биржи + Settings:
    """
    WS_URL: str
    WS_STREAMS_URL: str
    API_URL: str
    INTERVAL: int

    class Config:
        env_prefix = "BINANCE_"
