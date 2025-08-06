import datetime as dt
import logging
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, Security
from geopy.distance import geodesic
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid6 import uuid7

from .depends import validate_activity_level, verify_api_key
from .dto import GeoSearchDTO, OrganizationCreateDTO, OrganizationDTO, OrganizationUpdateDTO
from ..db.models import Activity, Building, Organization, OrganizationActivity, OrganizationPhone
from ..db.session import get_db

router = APIRouter(prefix="/organizations", tags=["Organizations"])

logger = logging.getLogger(__name__)


@router.get("/by_building/{building_id}/",
            response_model=List[OrganizationDTO],
            dependencies=[Security(verify_api_key)])
async def get_organizations_by_building(
        response: Response,
        building_id: UUID,
        session: AsyncSession = Depends(get_db)
) -> List[dict]:
    """
    
    :param building_id: 
    :param response: 
    :param session: 
    :return: 
    """
    stmt = select(Organization).where(
        Organization.building_id == building_id,
    )
    result = await session.execute(stmt)
    if not (organizations := result.scalars().all()):
        raise HTTPException(status_code=404, detail="No organizations found in this building")
    response.status_code = 200
    return [org.fields() for org in organizations]


@router.get("/by_activity/{activity_id}/",
            response_model=List[OrganizationDTO],
            dependencies=[Security(verify_api_key)])
async def get_organizations_by_activity(
        response: Response,
        activity_id: UUID,
        session: AsyncSession = Depends(get_db)
) -> List[dict]:
    """Get all organizations associated with a specific activity"""
    await validate_activity_level(activity_id, session)
    stmt = (
        select(Organization)
        .join(OrganizationActivity, Organization.id == OrganizationActivity.organization_id)
        .where(OrganizationActivity.activity_id == activity_id)
    )
    result = await session.execute(stmt)
    organizations = result.scalars().all()
    if not organizations:
        raise HTTPException(status_code=404, detail="No organizations found for this activity")
    response.status_code = 200
    return [org.fields() for org in organizations]


@router.post("/by_geo/",
             response_model=List[OrganizationDTO],
             dependencies=[Security(verify_api_key)])
async def get_organizations_by_geo(
        response: Response,
        dto: GeoSearchDTO,
        session: AsyncSession = Depends(get_db)
) -> List[dict]:
    """Get organizations within a radius or rectangular area"""
    if dto.radius_km is not None:
        # Circular search
        result = await session.execute(select(Building))
        buildings = result.scalars().all()
        valid_building_ids = []
        center = (dto.latitude, dto.longitude)
        for building in buildings:
            building_loc = (building.latitude, building.longitude)
            distance = geodesic(center, building_loc).kilometers
            if distance <= dto.radius_km:
                valid_building_ids.append(building.id)
    elif all([dto.lat_min, dto.lat_max, dto.lon_min, dto.lon_max]):
        stmt = select(Building).where(
            Building.latitude.between(dto.lat_min, dto.lat_max),
            Building.longitude.between(dto.lon_min, dto.lon_max),
        )
        result = await session.execute(stmt)
        valid_building_ids = [b.id for b in result.scalars().all()]
    else:
        raise HTTPException(status_code=400, detail="Provide either radius_km or all rectangular coordinates")

    if not valid_building_ids:
        raise HTTPException(status_code=404, detail="No buildings found in the specified area")

    stmt = select(Organization).where(Organization.building_id.in_(valid_building_ids))
    result = await session.execute(stmt)
    organizations = result.scalars().all()
    response.status_code = 200
    return [org.fields() for org in organizations]


@router.get("/{organization_id}/",
            response_model=OrganizationDTO,
            dependencies=[Security(verify_api_key)])
async def get_organization_by_id(
        response: Response,
        organization_id: UUID,
        session: AsyncSession = Depends(get_db)
) -> dict:
    """Get organization details by ID"""
    organization = await session.get(Organization, organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    response.status_code = 200
    return organization.fields()


@router.get("/by_activity_tree/{activity_id}/",
            response_model=List[OrganizationDTO],
            dependencies=[Security(verify_api_key)])
async def get_organizations_by_activity_tree(
        response: Response,
        activity_id: UUID,
        session: AsyncSession = Depends(get_db)
) -> List[dict]:
    """Get organizations by activity and its descendants (up to level 3)"""
    await validate_activity_level(activity_id, session)

    activity_ids = [activity_id]
    current_level = 1
    while current_level < 3:
        stmt = select(Activity.id).where(
            Activity.parent_id.in_(activity_ids),
            Activity.level <= 3,
        )
        result = await session.execute(stmt)
        if not (child_ids := result.scalars().all()):
            break
        activity_ids.extend(child_ids)
        current_level += 1

    stmt = (
        select(Organization)
        .join(OrganizationActivity, Organization.id == OrganizationActivity.organization_id)
        .where(OrganizationActivity.activity_id.in_(activity_ids))
        .distinct()
    )
    result = await session.execute(stmt)
    if not (organizations := result.scalars().all()):
        raise HTTPException(status_code=404, detail="No organizations found for this activity tree")
    response.status_code = 200
    return [org.fields() for org in organizations]


@router.get("/by_name/{name}/",
            response_model=List[OrganizationDTO],
            dependencies=[Security(verify_api_key)])
async def get_organizations_by_name(
        response: Response,
        name: str,
        session: AsyncSession = Depends(get_db)
) -> List[dict]:
    """Search organizations by name (partial match)"""
    stmt = select(Organization).where(Organization.name.ilike(f"%{name}%"))
    result = await session.execute(stmt)
    if not (organizations := result.scalars().all()):
        raise HTTPException(status_code=404, detail="No organizations found with this name")
    response.status_code = 200
    return [org.fields() for org in organizations]


@router.post("/",
             response_model=OrganizationDTO,
             dependencies=[Security(verify_api_key)])
async def create_organization(
        response: Response,
        dto: OrganizationCreateDTO,
        session: AsyncSession = Depends(get_db)
) -> dict:
    """Create a new organization"""
    if not (building := await session.get(Building, dto.building_id)):
        raise HTTPException(status_code=404, detail="Building not found")

    for activity_id in dto.activity_ids:
        await validate_activity_level(activity_id, session)

    organization = Organization(
        id=uuid7(),
        name=dto.name,
        building_id=dto.building_id,
        created_at=dt.datetime.now(dt.UTC),
    )
    session.add(organization)

    # Add phone numbers
    for phone in dto.phone_numbers:
        phone_entry = OrganizationPhone(
            organization_id=organization.id,
            phone_number=phone,
            created_at=dt.datetime.now(dt.UTC),
        )
        session.add(phone_entry)

    # Add activities
    for activity_id in dto.activity_ids:
        activity_entry = OrganizationActivity(
            organization_id=organization.id,
            activity_id=activity_id,
            created_at=dt.datetime.now(dt.UTC),
        )
        session.add(activity_entry)

    await session.commit()
    response.status_code = 201
    return organization.fields()


@router.patch("/{organization_id}/",
              response_model=OrganizationDTO,
              dependencies=[Security(verify_api_key)])
async def update_organization(
        response: Response,
        organization_id: UUID,
        dto: OrganizationUpdateDTO,
        session: AsyncSession = Depends(get_db)
) -> dict:
    """Update an organization"""
    if not (organization := await session.get(Organization, organization_id)):
        raise HTTPException(status_code=404, detail="Organization not found")

    update_data = dto.model_dump(exclude_unset=True)

    # Update main organization fields
    for field, value in update_data.items():
        if field in ["name", "building_id"]:
            if field == "building_id":
                building = await session.get(Building, value)
                if not building:
                    raise HTTPException(status_code=404, detail="Building not found")
            setattr(organization, field, value)

    # Update phone numbers
    if "phone_numbers" in update_data:
        # Mark existing phones as inactive
        stmt = select(OrganizationPhone).where(
            OrganizationPhone.organization_id == organization_id
        )
        result = await session.execute(stmt)
        for phone in result.scalars().all():
            session.add(phone)

        # Add new phone numbers
        for phone in update_data["phone_numbers"]:
            phone_entry = OrganizationPhone(
                organization_id=organization.id,
                phone_number=phone,
                created_at=dt.datetime.now(dt.UTC),
            )
            session.add(phone_entry)

    # Update activities
    if "activity_ids" in update_data:
        # Validate new activities
        for activity_id in update_data["activity_ids"]:
            await validate_activity_level(activity_id, session)

        # Mark existing activities as inactive
        stmt = select(OrganizationActivity).where(
            OrganizationActivity.organization_id == organization_id,
        )
        result = await session.execute(stmt)
        for activity in result.scalars().all():
            session.add(activity)

        # Add new activities
        for activity_id in update_data["activity_ids"]:
            activity_entry = OrganizationActivity(
                organization_id=organization.id,
                activity_id=activity_id,
                created_at=dt.datetime.now(dt.UTC),
            )
            session.add(activity_entry)

    session.add(organization)
    await session.commit()
    response.status_code = 200
    return organization.fields()


@router.delete("/{organization_id}/",
               response_model=OrganizationDTO,
               dependencies=[Security(verify_api_key)])
async def delete_organization(
        response: Response,
        organization_id: UUID,
        session: AsyncSession = Depends(get_db)
) -> dict:
    """Soft delete an organization"""
    organization = await Organization.get_or_404(id=organization_id, session=session)
    if not await Organization.delete_where(id=organization_id, session=session):
        raise HTTPException(status_code=404, detail="Organization not found")

    response.status_code = 200
    return organization.fields()
