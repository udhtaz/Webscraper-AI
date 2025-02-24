from fastapi import Form
from typing import Literal, Optional
from pydantic import BaseModel, Field


def get_valid_models():
    return [
        "gpt-4o", 
        "gemma2-9b-it", 
        "deepseek-r1-distill-llama-70b", 
        "qwen-2.5-32b", 
        "llama-3.3-70b-versatile", 
        "mixtral-8x7b-32768"
    ]

class AIInputModel:
    def __init__(
        self,
        country: str = Form(..., min_length=3, max_length=60, example="ghana"),
        city: str = Form(..., min_length=3, max_length=180, example="accra"),
        is_db: bool = Form(False, example=False),
        model: Literal[
            "gpt-4o", 
            "gemma2-9b-it", 
            "deepseek-r1-distill-llama-70b", 
            "qwen-2.5-32b", 
            "llama-3.3-70b-versatile", 
            "mixtral-8x7b-32768"
        ] = Form("gpt-4o", example="gpt-4o"),
    ):
        self.country = country
        self.city = city
        self.is_db = is_db
        self.model = model


class EventCreate(BaseModel):
    event_name: str = Field(..., min_length=3, max_length=255)
    event_category: str
    eventbrite_id: str
    event_location: str
    venue: str
    event_time: str  # Stored as string for flexibility
    event_url: str
    image_url: Optional[str] = None
    model: str

class EventUpdate(BaseModel):
    event_name: Optional[str] = None
    event_category: Optional[str] = None
    eventbrite_id: Optional[str] = None
    event_location: Optional[str] = None
    venue: Optional[str] = None
    event_time: Optional[str] = None
    event_url: Optional[str] = None
    image_url: Optional[str] = None
    model: Optional[str] = None

class EventResponse(BaseModel):
    id: int
    event_name: str
    event_category: str
    eventbrite_id: str
    event_location: str
    venue: str
    event_time: str
    event_url: str
    image_url: Optional[str]
    model: str

    class Config:
        orm_mode = True 
