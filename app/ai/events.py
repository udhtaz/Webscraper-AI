from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from .schemas import AIInputModel
from .service import AIService

scraper_router = APIRouter()
service = AIService()

@scraper_router.post("/generate-events/")
async def generate_events(
    region_data: AIInputModel = Depends(),
    session: AsyncSession = Depends(get_session),
):

    return await service.generate_events_table(region_data, session)
