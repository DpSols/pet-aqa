import os
from typing import Literal

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class KafkaSettings(BaseModel):
    bootstrap_servers: str = "localhost:9092"
    consumer_group: str = "test-group"


class PostgresSettings(BaseModel):
    dsn: str = "postgresql://testuser:testpass@localhost:5432/testdb"


class ApiSettings(BaseModel):
    base_url: str = "https://petstore.swagger.io/v2"


class WebSettings(BaseModel):
    base_url: str = "https://www.saucedemo.com"
    headless: bool = True
    record_video: bool = False


class MobileSettings(BaseModel):
    appium_url: str = "http://localhost:4723"
    platform: Literal["android", "ios"] = "android"
    device_name: str = "emulator-5554"
    app_path: str = "/path/to/demo-app.apk"


class Settings(BaseSettings):
    kafka: KafkaSettings = KafkaSettings()
    postgres: PostgresSettings = PostgresSettings()
    api: ApiSettings = ApiSettings()
    web: WebSettings = WebSettings()
    mobile: MobileSettings = MobileSettings()

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=os.getenv("ENV_FILE", ".env"),
        env_file_encoding="utf-8",
    )
