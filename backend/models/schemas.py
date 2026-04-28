from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class PetProfile(BaseModel):
  petType: str
  petName: str
  ageYears: int = 0
  ageMonths: int = 0
  sex: str = ""
  breed: str = ""
  source: str = ""
  role: str = ""
  commandsKnown: List[str] = []
  struggles: List[str] = []

class AskRequest(BaseModel):
  question: str
  petProfile: PetProfile

class AskResponse(BaseModel):
  answer: str
  confidence: float
  source: str
  retrieved_context: str

class TrainingFeedbackRequest(BaseModel):
  command: str
  duration: int
  notes: str
  petProfile: PetProfile

class TrainingFeedbackResponse(BaseModel):
  feedback: str
  confidence: float

class ChecklistRequest(BaseModel):
  petProfile: PetProfile

class ChecklistItem(BaseModel):
  title: str
  time: str
  subtitle: Optional[str] = None
  category: str

class ChecklistResponse(BaseModel):
  items: List[ChecklistItem]
