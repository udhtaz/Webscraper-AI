from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.db import get_session, Event
from .schemas import EventCreate, EventUpdate, EventResponse

crud_router = APIRouter()

@crud_router.post("/events/", response_model=EventResponse, status_code=201)
async def create_event(event_data: EventCreate, session: AsyncSession = Depends(get_session)):
    """
    Creates a new event in the database.
    """
    new_event = Event(**event_data.model_dump()) 

    session.add(new_event)
    await session.commit()
    await session.refresh(new_event)  # Retrieve auto-generated ID

    return new_event


@crud_router.get("/events/", response_model=list[EventResponse])
async def get_all_events(session: AsyncSession = Depends(get_session)):
    """
    Fetches all events from the database.
    """
    result = await session.exec(select(Event))
    events = result.all()

    return events


@crud_router.get("/events/{event_id}", response_model=EventResponse)
async def get_event(event_id: int, session: AsyncSession = Depends(get_session)):
    """
    Fetches a specific event by ID.
    """
    event = await session.get(Event, event_id)

    if not event:
        raise HTTPException(status_code=404, detail="Event ID not found")

    return event


@crud_router.put("/events/{event_id}", response_model=EventResponse)
async def update_event(event_id: int, event_data: EventUpdate, session: AsyncSession = Depends(get_session)):
    """
    Updates an existing event.
    """
    event = await session.get(Event, event_id)

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Update only fields provided in request
    event_data_dict = event_data.model_dump(exclude_unset=True)
    for key, value in event_data_dict.items():
        setattr(event, key, value)

    await session.commit()
    await session.refresh(event)

    return event


@crud_router.delete("/events/{event_id}", status_code=204)
async def delete_event(event_id: int, session: AsyncSession = Depends(get_session)):
    """
    Deletes an event by ID.
    """
    event = await session.get(Event, event_id)

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    await session.delete(event)
    await session.commit()

    return {"message": "Event deleted successfully"}