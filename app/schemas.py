from pydantic import BaseModel
from typing import Literal
from datetime import datetime
from uuid import UUID


class DemographicData(BaseModel):
    id: UUID
    
    @field_validator("id")
    def validate_uuid7(cls, v: UUID):
        if v.version != 7:
            raise ValueError("UUID must be version 7")
        return v

    name: str
    gender: str
    gender_probability: float
    age: int
    age_group: str
    country_id: str
    country_name: str
    country_probability: float
    created_at: datetime


class ErrorResponse(BaseModel):
    status: Literal["error"]
    message: str


class SuccessResponse(BaseModel):
    status: Literal["success"]
    page: int
    limit: int
    total: int
    data: DemographicData
    
