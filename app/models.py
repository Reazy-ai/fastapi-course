from datetime import datetime

from sqlalchemy import Boolean, Column, TIMESTAMP, func
from sqlmodel import Field, SQLModel, Relationship


class Post(SQLModel, table=True):
    __tablename__ = "posts"

    id: int = Field(primary_key=True, nullable=False)
    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    published: bool = Field(default=True, sa_column=Column(Boolean, server_default="true"))
    created_at: datetime = Field(sa_column=Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False))
    owner_id: int = Field(foreign_key="users.id", ondelete="CASCADE", nullable=False)
    owner: "User" = Relationship()


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(primary_key=True, nullable=False)
    email: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    created_at: datetime = Field(sa_column=Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False))

class Vote(SQLModel, table=True):
    __tablename__ = "votes"

    user_id: int = Field(foreign_key="users.id", ondelete="CASCADE", nullable=False, primary_key=True)
    post_id: int = Field(foreign_key="posts.id", ondelete="CASCADE", nullable=False, primary_key=True)