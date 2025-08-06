from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.config import settings
from ..db.models import Activity

# Static API key for authentication
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != settings.SECRET_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return api_key


# Helper function to check activity level
async def validate_activity_level(activity_id: UUID, session: AsyncSession) -> bool:
    activity = await session.get(Activity, activity_id)
    if not activity or activity.level > 3:
        raise HTTPException(status_code=400, detail="Activity level exceeds maximum (3) or not found")
    return True
