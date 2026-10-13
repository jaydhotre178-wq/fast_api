# ORM = object relational mapping is a technique that allows you to interact with a database using object-oriented programming concepts. It provides a way to map database tables to classes and rows to objects, making it easier to work with data in a more intuitive way.

from collections.abc import AsyncGenerator
import datetime
import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import inspect
from fastapi_users.db import SQLAlchemyUserDatabase, SQLAlchemyBaseUserTableUUID 
from fastapi import Depends


# for production ready database you simply change the database url to the production database url and it will work seamlessly without any changes in the code.
DATABASE_URL = "sqlite+aiosqlite:///./test.db"

class Base(DeclarativeBase):
    pass

class User(Base, SQLAlchemyBaseUserTableUUID):
   post = relationship("Post", back_populates="user")



class Post(Base):
    __tablename__ = "posts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    caption = Column(Text)
    url = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_name = Column("fire_name", String, nullable=False)
    crated_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    user = relationship("User", back_populates="post")
    
    
# create an async engine to connect to the database

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        if engine.dialect.name == "sqlite":
            columns = await conn.run_sync(
                lambda sync_conn: inspect(sync_conn).get_columns("posts")
            )
            if not any(column["name"] == "user_id" for column in columns):
                await conn.exec_driver_sql(
                    'ALTER TABLE posts ADD COLUMN user_id CHAR(36) REFERENCES "user"(id)'
                )
        


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
        
        

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)