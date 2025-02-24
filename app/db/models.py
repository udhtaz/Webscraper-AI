import uuid
from datetime import datetime
import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, SQLModel, Integer

class User(SQLModel, table=True):
    __tablename__ = "users"
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    username: str = Field(nullable=False)
    email: str = Field(nullable=False, unique=True)
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    role: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False, server_default="user")
    )
    is_verified: bool = Field(default=False)
    password_hash: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False), exclude=True
    )
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    def __repr__(self):
        return (
            f"<User(username={self.username}, first_name={self.first_name}, "
            f"last_name={self.last_name}, role={self.role})>"
        )


class Event(SQLModel, table=True):
    __tablename__= "events"

    id: int = Field(
        sa_column=Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    )
    event_name: str = Field(nullable=False)
    event_category: str = Field(nullable=False)
    eventbrite_id: str = Field(nullable=False, unique=True)  # Eventbrite ID
    event_location: str = Field(nullable=False)
    venue: str = Field(nullable=False)
    event_time: str = Field(nullable=False)  # Stored as string for flexibility
    event_url: str = Field(nullable=False)
    image_url: str = Field(nullable=True)
    event_description: str = Field(nullable=True)
    model: str = Field(nullable=False)
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now)
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now, onupdate=datetime.now)
    )

    def __repr__(self):
        return (
            f"<Event(id={self.id}, name={self.event_name}, category={self.event_category}, "
            f"venue={self.venue}, time={self.event_time})>"
        )
