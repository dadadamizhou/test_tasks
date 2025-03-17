import base64
import os
from pathlib import PosixPath, Path
from typing import Optional, Any, List

from pydantic import AnyUrl, AnyHttpUrl, field_validator
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = 'task'
    BACKEND_CORS_ORIGINS: List[str] = []
    HOST: str = 'http://127.0.0.1'
    OPENAPI_URL: str = "/openapi.json"
    BASE_DIR: Optional[PosixPath] = Path(__file__).absolute().parent.parent

    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_URI: Optional[str] = None

    @field_validator("DB_URI")
    def assemble_db_connection(cls, v: Optional[str], info: FieldValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        return str(AnyUrl.build(
            scheme="mysql+pymysql",
            username=info.data["DB_USER"],
            password=info.data["DB_PASSWORD"],
            host=info.data["DB_HOST"],
            port=info.data["DB_PORT"],
            path=f"{info.data['DB_NAME'] or ''}",
        ))

    class Config:
        case_sensitive = True

settings = Settings()
