from datetime import UTC, datetime
from typing import Any, Optional as O
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy import DateTime, ForeignKey as FK, Text, Float
from sqlalchemy.orm import Mapped as M
from sqlalchemy.orm import mapped_column as col
from sqlalchemy.orm import relationship

from .base import Base
from ..core.error import E


class Building(Base):
    __tablename__ = "building"

    address: M[str] = col(Text, nullable=False, comment="Адрес здания")
    latitude: M[float] = col(Float, nullable=False, comment="Широта")
    longitude: M[float] = col(Float, nullable=False, comment="Долгота")
    created_at: M[datetime] = col(DateTime(timezone=True), default=datetime.now(UTC), comment="Дата создания")

    organizations: M[Any] = relationship("Organization", back_populates="building")

    er_404 = E.ER_NOT_BUILDING


class Activity(Base):
    __tablename__ = "activity"

    name: M[str] = col(Text, nullable=False, comment="Название деятельности")
    parent_id: M[O[UUID]] = col(FK("activity.id", ondelete="CASCADE"), nullable=True, comment="Родительская деятельность")
    level: M[int] = col(sa.Integer, nullable=False, default=1, comment="Уровень вложенности (1-3)")
    created_at: M[datetime] = col(DateTime(timezone=True), default=datetime.now(UTC), comment="Дата создания")

    organizations: M[Any] = relationship("OrganizationActivity", back_populates="activity")

    er_404 = E.ER_NOT_ACTIVITY


class Organization(Base):
    __tablename__ = "organization"

    name: M[str] = col(Text, nullable=False, comment="Название организации")
    building_id: M[UUID] = col(FK("building.id", ondelete="RESTRICT"), nullable=False, comment="Здание")
    created_at: M[datetime] = col(DateTime(timezone=True), default=datetime.now(UTC), comment="Дата создания")

    building: M[Any] = relationship("Building", back_populates="organizations")
    phone_numbers: M[Any] = relationship("OrganizationPhone", back_populates="organization")
    activities: M[Any] = relationship("OrganizationActivity", back_populates="organization")

    er_404 = E.ER_NOT_ORGANIZATION


class OrganizationPhone(Base):
    __tablename__ = "organization_phone"

    organization_id: M[UUID] = col(FK("organization.id", ondelete="CASCADE"), nullable=False, comment="Организация")
    phone_number: M[str] = col(Text, nullable=False, comment="Номер телефона")
    created_at: M[datetime] = col(DateTime(timezone=True), default=datetime.now(UTC), comment="Дата создания")

    organization: M[Any] = relationship("Organization", back_populates="phone_numbers")

    er_404 = E.ER_NOT_ORGANIZATION_PHONE


class OrganizationActivity(Base):
    __tablename__ = "organization_activity"

    organization_id: M[UUID] = col(FK("organization.id", ondelete="CASCADE"), nullable=False, comment="Организация")
    activity_id: M[UUID] = col(FK("activity.id", ondelete="RESTRICT"), nullable=False, comment="Деятельность")
    created_at: M[datetime] = col(DateTime(timezone=True), default=datetime.now(UTC), comment="Дата создания")

    organization: M[Any] = relationship("Organization", back_populates="activities")
    activity: M[Any] = relationship("Activity", back_populates="organizations")

    er_404 = E.ER_NOT_ORGANIZATION_ACTIVITY
