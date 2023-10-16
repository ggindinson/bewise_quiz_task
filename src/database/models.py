import datetime
from typing import Annotated, Any, Dict, List, Sequence, Type, TypeVar

from sqlalchemy import BigInteger, DateTime, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, registry

from utils.repr import PrettyRepr

# Define custom annotations
bigint = Annotated[int, "big integer"]
T = TypeVar("T")


# Define declarative base
class Base(DeclarativeBase, PrettyRepr):
    __table_args__ = {"extend_existing": True}
    __abstract__ = True

    registry = registry(
        type_annotation_map={
            bigint: BigInteger,
        }
    )

    id: Any
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.datetime.now()
    )

    @classmethod
    async def get_all(cls: Type[T], session: AsyncSession) -> Sequence[T]:
        result = await session.execute(select(cls))
        return result.scalars().all()

    @classmethod
    async def create(
        cls: Type[T],
        session: AsyncSession,
        params: List[Dict[str, Any]] | Dict[str, Any],
    ) -> T:
        result = await session.execute(insert(cls).values(params).returning(cls))
        await session.commit()
        return result.scalar()

    @classmethod
    async def get_by_id(
        cls: Type[T], session: AsyncSession, model_id: int | str
    ) -> T | None:
        row = await session.execute(select(cls).where(cls.id == model_id))
        return row.scalar_one_or_none()

    @classmethod
    async def get_all(cls: Type[T], session: AsyncSession) -> Sequence[T]:
        result = await session.execute(select(cls))
        return result.scalars().all()

    @classmethod
    async def create(
        cls: Type[T],
        session: AsyncSession,
        params: List[Dict[str, Any]] | Dict[str, Any],
    ) -> T:
        result = await session.execute(insert(cls).values(params).returning(cls))
        await session.commit()
        return result.scalar()


class Questions(Base):
    __tablename__ = "questions"

    id: Mapped[bigint] = mapped_column(primary_key=True)
    answer: Mapped[str]
    question: Mapped[str]
    category_id: Mapped[int]

    @classmethod
    async def create_unique_and_return(
        cls, session: AsyncSession, data: List[Dict[str, Any]]
    ) -> List["Questions"]:
        result = await session.execute(
            insert(Questions)
            .values(data)
            .on_conflict_do_nothing(index_elements=["id"])
            .returning(Questions)
        )
        await session.commit()
        return result.scalars().all()
