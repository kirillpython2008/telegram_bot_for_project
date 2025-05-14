import asyncio

from sqlalchemy import select, delete
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from mistral import positive_or_negative

async_engine = create_async_engine(url="sqlite+aiosqlite:///db.db")
async_session_factory = async_sessionmaker(bind=async_engine)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(nullable=True)
    feedback: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[bool] = mapped_column(nullable=True)
    items: Mapped[str] = mapped_column(nullable=True)
    count_orders: Mapped[int] = mapped_column(nullable=True, default=0)


async def create_tables():
    async with async_engine.connect() as connect:
        await connect.run_sync(User.metadata.drop_all)
        await connect.run_sync(User.metadata.create_all)


class CRUD:
    @staticmethod
    async def insert_user(user_id: str, username: str=None, feedback: str=None, status:str=None):
        async with async_session_factory() as session:
            user = User(user_id=user_id, username=username, feedback=feedback, status=status)
            session.add(user)

            await session.commit()

    @staticmethod
    async def insert_feedback(user_id: str, text_feedback: str):
        async with async_session_factory() as session:
            mistral_answer = await positive_or_negative(text_feedback=text_feedback)

            query = select(User).where(User.user_id == user_id)
            result = await session.execute(query)
            user = result.one()[0]

            user.feedback = text_feedback
            user.status = mistral_answer

            await session.commit()

    @staticmethod
    async def check_user(user_id: str):
        async with async_session_factory() as session:
            query = select(User).where(User.user_id == user_id)
            result = await session.execute(query)
            user = result.one_or_none()
            return bool(user) #True if there is user and else False

    @staticmethod
    async def read_user_items(user_id: str):
        async with async_session_factory() as session:
            query = select(User.items).where(User.user_id == user_id)
            result = await session.execute(query)
            items = result.one()[0]

            return items

    @staticmethod
    async def insert_bucket(user_id: str, item: str):
        async with async_session_factory() as session:
            query = select(User).where(User.user_id == user_id)
            result = await session.execute(query)
            user = result.one()[0]

            past_items = await CRUD.read_user_items(user_id=user_id)
            new_item = f"{past_items}|{item}"

            user.items = new_item

            await session.commit()

    @staticmethod
    async def delete_items(user_id: str):
        async with async_session_factory() as session:
            query = select(User).where(User.user_id == user_id)
            result = await session.execute(query)
            user = result.one()[0]

            user.items = None

            await session.commit()

    @staticmethod
    async def add_order(user_id: str):
        async with async_session_factory() as session:
            query = select(User).where(User.user_id == user_id)
            result = await session.execute(query)
            user = result.one()[0]

            user.count_orders += 1
            await session.commit()

    @staticmethod
    async def get_all_users():
        async with async_session_factory() as session:
            query = select(User)
            result = await session.execute(query)
            result = result.scalars().all()
            return len(result)

    @staticmethod
    async def get_all_orders():
        async with async_session_factory() as session:
            query = select(User.count_orders)
            result = await session.execute(query)
            result = result.scalars().all()

            return sum(result)

    @staticmethod
    async def get_negative_or_positive_feedback(positive: bool=False):
        async with async_session_factory() as session:
            if positive:
                query = select(User).where(User.status == True)
            else:
                query = select(User).where(User.status == False)

            result = await session.execute(query)
            result = result.scalars().all()

            return len(result)
