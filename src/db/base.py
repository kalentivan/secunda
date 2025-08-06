import logging
from typing import ClassVar, List, Optional, Self
from uuid import UUID

import uuid6
from sqlalchemy import Uuid, delete, select
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from starlette import status

from ..core.error import E

logger = logging.getLogger(__name__)


class Base(AsyncAttrs, DeclarativeBase):
    """Базовый класс моделей таблиц"""
    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid6.uuid7)

    er_404: ClassVar[E] = E.ER_NOT_ITEM  # ошибка, если запись не найдена
    joins: ClassVar[tuple[str, ...]] = tuple()  # связанные таблицы, данные из которых надо подгружать при запросе
    _exclude: ClassVar[tuple[str, ...]] = tuple()

    def fields(self) -> dict:
        return {
            column.key: getattr(self, column.key)
            for column in self.__table__.columns
        }

    @classmethod
    def get_manager(cls, name: str):
        return cls._decl_class_registry.get(name)

    @classmethod
    async def get_or_404(cls,
                         session: Optional[AsyncSession],
                         er_status=status.HTTP_404_NOT_FOUND, er_msg=None, **kwargs) -> Self:
        """
        Возвращает первый объект, соответствующий фильтру, или вызывает HTTPException 404.
        Пример: await User.get_or_404(id=1)
        """
        result = await session.execute(select(cls).filter_by(**kwargs))
        obj = result.scalar_one_or_none()
        if obj is None:
            raise cls.er_404.up_raise()
        return obj

    @classmethod
    async def get(cls,
                  session: AsyncSession,
                  **kwargs) -> Self:
        """
        Аналог Django get():
        - Вернёт один объект, если он найден
        - Поднимет ошибку, если найдено несколько
        - Поднимет ошибку, если не найден ни один
        """
        stmt = select(cls).filter_by(**kwargs)
        result = await session.execute(stmt)
        try:
            return result.scalar_one()
        except NoResultFound:
            return None
        except MultipleResultsFound:
            raise ValueError("Найдено более одного объекта.")

    @classmethod
    async def list(cls, session: AsyncSession, **kwargs) -> list:
        try:
            stmt = select(cls).filter_by(**kwargs)
            result = await session.execute(stmt)
            return list(result.scalars().all())
        except Exception as ex:
            logger.error(f"Ошибка в {cls.__name__}.list: {ex}", exc_info=True)
            return []

    @classmethod
    async def list_dict(cls, session: AsyncSession, **kwargs) -> List[dict]:
        # try:
        stmt = select(*cls.__table__.columns).filter_by(**kwargs)
        result = await session.execute(stmt)
        return [dict(note) for note in result.mappings().all()]
        # except Exception as ex:
        #     logger.error(f"Ошибка в {cls.__name__}.list_dict: {ex}", exc_info=True)
        #     return []

    @classmethod
    async def delete_where(cls, session: AsyncSession, **kwargs):
        """
        Удаляет объекты, соответствующие фильтру kwargs.
        Пример: await Meeting.delete_where(session=session, status=TStatus.OPEN)
        """
        try:
            stmt = (
                delete(cls)
                .where(*[getattr(cls, k) == v for k, v in kwargs.items()])
                .returning(cls.id)  # можно вернуть любые поля
            )
            result = await session.execute(stmt)
            await session.commit()
            deleted_count = len(result.fetchall())
            return deleted_count
        except Exception as ex:
            logger.error(f"Ошибка при удалении {cls.__name__}: {ex}", exc_info=True)
            raise

