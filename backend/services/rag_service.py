import os
from pathlib import Path

KNOWLEDGE_BASE_DIR = Path(__file__).parent.parent / "knowledge_base"

def get_relevant_docs(question: str, pet_type: str) -> tuple[str, str]:
  """
  Search knowledge base files for relevant content.
  Returns (retrieved_context, source_name)
  """
  question_lower = question.lower()

  # Determine which files to search based on pet type and question
  pet_prefix = "kitten" if pet_type.lower() == "cat" else "puppy"

  # Score each file by keyword matches
  file_scores = {}

  nutrition_keywords = [
    "feed", "food", "eat", "meal", "diet", "nutrition",
    "hungry", "portion", "kibble", "protein", "water"
  ]
  training_keywords = [
    "train", "potty", "sit", "stay", "come", "down",
    "command", "behavior", "accident", "crate", "learn",
    "teach", "obedient", "litter"
  ]
  health_keywords = [
    "vaccine", "vet", "sick", "health", "medicine",
    "medication", "flea", "worm", "spay", "neuter",
    "shot", "doctor", "ill", "symptom", "poison"
  ]

  keyword_map = {
    f"{pet_prefix}_nutrition.txt": nutrition_keywords,
    f"{pet_prefix}_training.txt": training_keywords,
    f"{pet_prefix}_health.txt": health_keywords,
  }

  for filename, keywords in keyword_map.items():
    score = sum(1 for kw in keywords if kw in question_lower)
    file_scores[filename] = score

  # Pick the best matching file, default to nutrition
  best_file = max(file_scores, key=file_scores.get)
  if file_scores[best_file] == 0:
    best_file = f"{pet_prefix}_nutrition.txt"

  # Read the file
  file_path = KNOWLEDGE_BASE_DIR / best_file
  try:
    content = file_path.read_text(encoding="utf-8")
    source_name = best_file.replace("_", " ").replace(".txt", "").title()
    return content, source_name
  except FileNotFoundError:
    return "", "PawPal+ knowledge base"
