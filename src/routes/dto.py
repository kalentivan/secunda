import datetime as dt
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class PhoneDTO(BaseModel):
    phone_number: str


class ActivityDTO(BaseModel):
    id: UUID
    name: str
    parent_id: Optional[UUID] = None
    level: int


class OrganizationDTO(BaseModel):
    id: UUID
    name: str
    building_id: UUID
    created_at: dt.datetime


class OrganizationCreateDTO(BaseModel):
    name: str
    building_id: UUID
    phone_numbers: List[str]
    activity_ids: List[UUID]


class OrganizationUpdateDTO(BaseModel):
    name: Optional[str] = None
    building_id: Optional[UUID] = None
    phone_numbers: Optional[List[str]] = None
    activity_ids: Optional[List[UUID]] = None


class GeoSearchDTO(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    radius_km: Optional[float] = None  # For circular search
    lat_min: Optional[float] = None  # For rectangular search
    lat_max: Optional[float] = None
    lon_min: Optional[float] = None
    lon_max: Optional[float] = None