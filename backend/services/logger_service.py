from datetime import datetime

# In-memory log store (will be replaced with Supabase on Day 3)
interaction_logs = []

def log_interaction(
  pet_name: str,
  query: str,
  retrieved_context: str,
  response: str,
  confidence: float,
  source: str
) -> dict:
  """Log an AI interaction to memory."""
  log_entry = {
    "id": len(interaction_logs) + 1,
    "pet_name": pet_name,
    "query": query,
    "retrieved_context": retrieved_context[:200],
    "response": response,
    "confidence": confidence,
    "source": source,
    "timestamp": datetime.utcnow().isoformat(),
  }
  interaction_logs.append(log_entry)
  print(f"[LOG] {log_entry['timestamp']} | "
        f"Pet: {pet_name} | "
        f"Confidence: {confidence} | "
        f"Query: {query[:50]}")
  return log_entry

def get_logs() -> list:
  """Return all interaction logs."""
  return interaction_logs
