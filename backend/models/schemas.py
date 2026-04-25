from datetime import date, datetime, time
from typing import Optional

from pydantic import BaseModel


class Pet(BaseModel):
    id: Optional[str] = None
    name: str
    species: str
    breed: Optional[str] = None
    age: Optional[int] = None
    owner_id: Optional[str] = None
    notes: Optional[str] = None


class Task(BaseModel):
    id: Optional[str] = None
    pet_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    due_date: Optional[date] = None
    due_time: Optional[time] = None
    priority: Optional[str] = None
    recurring: bool = False
    recurrence_pattern: Optional[str] = None
    completed: bool = False


class TrainingSession(BaseModel):
    id: Optional[str] = None
    pet_id: str
    title: str
    description: Optional[str] = None
    session_date: Optional[date] = None
    duration_minutes: Optional[int] = None
    progress_notes: Optional[str] = None


class AIInteraction(BaseModel):
    id: Optional[str] = None
    user_message: str
    ai_response: Optional[str] = None
    context: Optional[str] = None
    created_at: Optional[datetime] = None
