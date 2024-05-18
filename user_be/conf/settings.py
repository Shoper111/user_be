from enum import Enum

from pydantic_settings import BaseSettings


class LogLevel(str, Enum):
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'


class Env(str, Enum):
    LOCAL = 'LOCAL'
    STAGING = 'STAGING'
    PRODUCTION = 'PRODUCTION'


class Settings(BaseSettings):
    DEBUG: bool = False
    ENV: Env = Env.LOCAL
    PORT: int = 4000
    LOG_LEVEL: LogLevel = LogLevel.INFO
    ALLOWED_ORIGINS: str = 'http://localhost http://localhost:3000 http://127.0.0.1:3000'

    MONGODB_HOST: str = 'localhost'
    MONGODB_PORT: int = 27017
    MONGODB_USER: str = 'root'
    MONGODB_PASS: str = 'root'

    AWS_DEFAULT_REGION: str = 'eu-central-1'
    COGNITO_POOL_ID: str = 'eu-central-1_dLdSYcSiJ'
    S3_BUCKET_NAME: str = 'shoper-images'
    AWS_ACCESS_KEY_ID: str = 'AKIA44K56ADDO35SXUR2'
    AWS_SECRET_ACCESS_KEY: str = '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'

    SENTRY_DSN: str | None = None

    @property
    def mongodb_database_uri(self):
        if self.ENV == Env.LOCAL:
            return f'mongodb://{self.MONGODB_HOST}:{self.MONGODB_PORT}/?retryWrites=false'
        return (
            f'mongodb://{self.MONGODB_USER}:{self.MONGODB_PASS}@'
            f'{self.MONGODB_HOST}:{self.MONGODB_PORT}/?retryWrites=false'
        )