import json
import asyncio
import logging
from datetime import datetime
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from .models import Building, Activity, Organization, OrganizationPhone, OrganizationActivity
from src.core.config import settings

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Установка WindowsSelectorEventLoopPolicy для Windows
if hasattr(asyncio, 'WindowsSelectorEventLoopPolicy'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def load_json_fixtures(session: AsyncSession, json_file_path: str):
    """Load test data from a JSON file into the database."""
    try:
        # Clear existing data
        for table in [OrganizationActivity, OrganizationPhone, Organization, Activity, Building]:
            await session.execute(table.__table__.delete())
        await session.commit()
        logger.info("Existing data cleared.")

        # Read JSON file
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Load Buildings
        for building_data in data.get('buildings', []):
            building = Building(
                id=UUID(building_data['id']),
                address=building_data['address'],
                latitude=building_data['latitude'],
                longitude=building_data['longitude'],
                created_at=datetime.fromisoformat(building_data['created_at']),
            )
            session.add(building)
        await session.flush()
        logger.info("Buildings loaded.")

        # Load Activities
        for activity_data in data.get('activities', []):
            activity = Activity(
                id=UUID(activity_data['id']),
                name=activity_data['name'],
                parent_id=UUID(activity_data['parent_id']) if activity_data['parent_id'] else None,
                level=activity_data['level'],
                created_at=datetime.fromisoformat(activity_data['created_at']),
            )
            session.add(activity)
        await session.flush()
        logger.info("Activities loaded.")

        # Load Organizations
        for org_data in data.get('organizations', []):
            organization = Organization(
                id=UUID(org_data['id']),
                name=org_data['name'],
                building_id=UUID(org_data['building_id']),
                created_at=datetime.fromisoformat(org_data['created_at']),
            )
            session.add(organization)
        await session.flush()
        logger.info("Organizations loaded.")

        # Load Organization Phones
        for phone_data in data.get('organization_phones', []):
            phone = OrganizationPhone(
                organization_id=UUID(phone_data['organization_id']),
                phone_number=phone_data['phone_number'],
                created_at=datetime.fromisoformat(phone_data['created_at']),
            )
            session.add(phone)
        await session.flush()
        logger.info("Organization phones loaded.")

        # Load Organization Activities
        for org_activity_data in data.get('organization_activities', []):
            org_activity = OrganizationActivity(
                organization_id=UUID(org_activity_data['organization_id']),
                activity_id=UUID(org_activity_data['activity_id']),
                created_at=datetime.fromisoformat(org_activity_data['created_at']),
            )
            session.add(org_activity)
        await session.flush()
        logger.info("Organization activities loaded.")

        await session.commit()
        logger.info("JSON fixtures loaded successfully.")
    except Exception as e:
        logger.error(f"Error loading fixtures: {str(e)}")
        await session.rollback()
        raise

async def run_fixtures(session: AsyncSession, json_file_path: str = "static/fixtures.json"):
    """Run the JSON fixture loading process."""
    await load_json_fixtures(session, json_file_path)

if __name__ == "__main__":
    # Создаём асинхронный движок и сессию
    engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, echo=True)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async def main():
        async with async_session() as session:
            await run_fixtures(session)

    # Запускаем асинхронный цикл
    asyncio.run(main())
