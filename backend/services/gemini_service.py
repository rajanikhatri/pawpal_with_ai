import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_gemini(
  question: str,
  pet_profile: dict,
  retrieved_context: str
) -> tuple[str, float]:
  """
  Send question + pet profile + retrieved context to Gemini.
  Returns (answer, confidence_score)
  """
  pet_name = pet_profile.get("petName", "the pet")
  pet_type = pet_profile.get("petType", "dog")
  breed = pet_profile.get("breed", "mixed breed")
  age_years = pet_profile.get("ageYears", 0)
  age_months = pet_profile.get("ageMonths", 0)
  struggles = pet_profile.get("struggles", [])

  age_str = ""
  if age_years > 0 and age_months > 0:
    age_str = f"{age_years} years and {age_months} months"
  elif age_years > 0:
    age_str = f"{age_years} years"
  elif age_months > 0:
    age_str = f"{age_months} months"
  else:
    age_str = "unknown age"

  struggles_str = ", ".join(struggles) if struggles else "none mentioned"

  prompt = f"""You are PawPal+, a friendly and knowledgeable pet care
assistant for first-time pet owners. Answer the question below using
ONLY the provided knowledge base context. Be warm, clear, and
practical. Keep your answer under 100 words.

PET PROFILE:
- Name: {pet_name}
- Type: {pet_type}
- Breed: {breed}
- Age: {age_str}
- Known struggles: {struggles_str}

KNOWLEDGE BASE CONTEXT:
{retrieved_context}

QUESTION: {question}

IMPORTANT RULES:
- Use the pet's name ({pet_name}) naturally in your answer
- Only use information from the knowledge base context above
- If the context does not cover the question well, say so honestly
- Do not make up facts
- Keep it friendly and under 100 words
- End with one practical next step

ANSWER:"""

  try:
    response = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[{"role": "user", "content": prompt}],
      max_tokens=300,
      temperature=0.3,
    )
    answer = response.choices[0].message.content.strip()

    # Calculate confidence based on context relevance
    question_words = set(question.lower().split())
    context_words = set(retrieved_context.lower().split())
    overlap = len(question_words & context_words)
    confidence = min(0.95, max(0.60, overlap / max(len(question_words), 1) * 2))
    confidence = round(confidence, 2)

    return answer, confidence

  except Exception as e:
    return (
      f"I am having trouble connecting right now. "
      f"Please try again in a moment.",
      0.0
    )

def get_training_feedback(
  command: str,
  duration: int,
  notes: str,
  pet_profile: dict
) -> tuple[str, float]:
  """Generate AI feedback for a training session."""
  pet_name = pet_profile.get("petName", "your pet")
  pet_type = pet_profile.get("petType", "dog")

  prompt = f"""You are PawPal+, a friendly pet training assistant.
A first-time {pet_type} owner just completed a training session.
Give warm, encouraging, practical feedback in under 80 words.

Session details:
- Pet name: {pet_name}
- Command practiced: {command}
- Duration: {duration} minutes
- Owner notes: {notes}

Give specific advice based on what they reported.
Start with something encouraging. End with one tip.

FEEDBACK:"""

  try:
    response = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[{"role": "user", "content": prompt}],
      max_tokens=300,
      temperature=0.3,
    )
    feedback = response.choices[0].message.content.strip()
    return feedback, 0.85
  except Exception:
    return (
      f"Great work practicing {command} with {pet_name}! "
      f"Consistency is the key to success. "
      f"Try 2-3 short sessions daily for best results.",
      0.70
    )
