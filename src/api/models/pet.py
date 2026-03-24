from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Category(BaseModel):
    id: int = 0
    name: str = ""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)


class Tag(BaseModel):
    id: int = 0
    name: str = ""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)


class Pet(BaseModel):
    id: int | None = None
    name: str = Field(...)
    photo_urls: list[str] = Field(default_factory=list, alias="photoUrls")
    category: Category | None = None
    tags: list[Tag] = Field(default_factory=list)
    status: Literal["available", "pending", "sold"] = "available"

    model_config = ConfigDict(extra="ignore", populate_by_name=True)
