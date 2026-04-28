from fastapi import APIRouter, HTTPException
from models.schemas import (
  AskRequest, AskResponse,
  TrainingFeedbackRequest, TrainingFeedbackResponse,
  ChecklistRequest, ChecklistResponse, ChecklistItem
)
from services.rag_service import get_relevant_docs
from services.gemini_service import ask_gemini, get_training_feedback
from services.logger_service import log_interaction, get_logs

router = APIRouter()

@router.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):
  """RAG endpoint: retrieve context then ask Gemini."""
  if not request.question.strip():
    raise HTTPException(status_code=400, detail="Question cannot be empty")

  pet_type = request.petProfile.petType
  question = request.question.strip()

  # Step 1: Retrieve relevant context from knowledge base
  retrieved_context, source = get_relevant_docs(question, pet_type)

  if not retrieved_context:
    raise HTTPException(
      status_code=500,
      detail="Could not retrieve knowledge base context"
    )

  # Step 2: Send to Gemini with context
  answer, confidence = ask_gemini(
    question=question,
    pet_profile=request.petProfile.model_dump(),
    retrieved_context=retrieved_context
  )

  # Step 3: Log the interaction
  log_interaction(
    pet_name=request.petProfile.petName,
    query=question,
    retrieved_context=retrieved_context,
    response=answer,
    confidence=confidence,
    source=source
  )

  return AskResponse(
    answer=answer,
    confidence=confidence,
    source=source,
    retrieved_context=retrieved_context[:300]
  )

@router.post("/training-feedback",
             response_model=TrainingFeedbackResponse)
async def training_feedback(request: TrainingFeedbackRequest):
  """Generate AI feedback for a training session."""
  feedback, confidence = get_training_feedback(
    command=request.command,
    duration=request.duration,
    notes=request.notes,
    pet_profile=request.petProfile.model_dump()
  )

  log_interaction(
    pet_name=request.petProfile.petName,
    query=f"Training feedback: {request.command}",
    retrieved_context="Training session data",
    response=feedback,
    confidence=confidence,
    source="Training feedback engine"
  )

  return TrainingFeedbackResponse(
    feedback=feedback,
    confidence=confidence
  )

@router.post("/checklist", response_model=ChecklistResponse)
async def generate_checklist(request: ChecklistRequest):
  """Generate a daily checklist based on pet profile."""
  profile = request.petProfile
  pet_type = profile.petType.lower()
  age_months = profile.ageMonths + (profile.ageYears * 12)

  if pet_type == "cat":
    items = [
      ChecklistItem(title="Morning feeding",
                    time="7:00 AM", category="feeding"),
      ChecklistItem(title="Clean litter box",
                    time="8:00 AM", category="hygiene"),
      ChecklistItem(title="Midday feeding",
                    time="12:00 PM", category="feeding",
                    subtitle="Wet food recommended"),
      ChecklistItem(title="Play session",
                    time="5:00 PM", category="exercise",
                    subtitle="10-15 min wand toy"),
      ChecklistItem(title="Evening feeding",
                    time="6:00 PM", category="feeding"),
      ChecklistItem(title="Fresh water check",
                    time="8:00 PM", category="hygiene"),
    ]
  else:
    if age_months < 6:
      items = [
        ChecklistItem(title="Morning feeding",
                      time="7:00 AM", category="feeding",
                      subtitle="Puppy kibble 3x daily"),
        ChecklistItem(title="Potty break",
                      time="8:00 AM", category="potty"),
        ChecklistItem(title="Training session",
                      time="10:00 AM", category="training",
                      subtitle="5 min: practice sit and stay"),
        ChecklistItem(title="Midday feeding",
                      time="12:00 PM", category="feeding"),
        ChecklistItem(title="Potty break",
                      time="2:00 PM", category="potty"),
        ChecklistItem(title="Evening feeding",
                      time="6:00 PM", category="feeding"),
        ChecklistItem(title="Potty break",
                      time="8:00 PM", category="potty"),
      ]
    else:
      items = [
        ChecklistItem(title="Morning feeding",
                      time="7:00 AM", category="feeding"),
        ChecklistItem(title="Morning walk",
                      time="8:00 AM", category="exercise",
                      subtitle="20-30 minutes"),
        ChecklistItem(title="Training session",
                      time="11:00 AM", category="training",
                      subtitle="10 min: practice commands"),
        ChecklistItem(title="Evening feeding",
                      time="6:00 PM", category="feeding"),
        ChecklistItem(title="Evening walk",
                      time="7:00 PM", category="exercise",
                      subtitle="20-30 minutes"),
      ]

  return ChecklistResponse(items=items)

@router.get("/logs")
async def get_interaction_logs():
  """Return all logged AI interactions."""
  return get_logs()
