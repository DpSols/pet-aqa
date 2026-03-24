from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Order(BaseModel):
    id: int | None = None
    pet_id: int = Field(..., alias="petId")
    quantity: int = 1
    ship_date: datetime | None = Field(default=None, alias="shipDate")
    status: Literal["placed", "approved", "delivered"] = "placed"
    complete: bool = False

    model_config = ConfigDict(extra="ignore", populate_by_name=True)


class ApiResponse(BaseModel):
    code: int = 0
    type: str = ""
    message: str = ""

    model_config = ConfigDict(extra="ignore")
