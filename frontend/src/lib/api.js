const API_BASE = import.meta.env.VITE_API_URL ? `${import.meta.env.VITE_API_URL}/api` : "http://localhost:8000/api"

export async function askAI(question, petProfile) {
  const response = await fetch(`${API_BASE}/ai/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, petProfile }),
  })
  if (!response.ok) throw new Error("API request failed")
  return response.json()
}

export async function getChecklist(petProfile) {
  const response = await fetch(`${API_BASE}/ai/checklist`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ petProfile }),
  })
  if (!response.ok) throw new Error("API request failed")
  return response.json()
}

export async function getTrainingFeedback(command, duration, notes, petProfile) {
  const response = await fetch(`${API_BASE}/ai/training-feedback`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ command, duration, notes, petProfile }),
  })
  if (!response.ok) throw new Error("API request failed")
  return response.json()
}
