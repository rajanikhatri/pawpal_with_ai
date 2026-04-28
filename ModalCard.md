# Model Card: PawPal+ AI

## Model Details

- **Model used:** OpenAI GPT-4o-mini
- **Access method:** OpenAI API via Python SDK
- **Retrieval method:** Keyword-based RAG over 6 local knowledge base files
- **Confidence scoring:** Keyword overlap between question and retrieved context, scaled 0.60 to 0.95
- **Logging:** Every AI interaction is recorded with query, retrieved context, response, confidence score, and timestamp

---

## Intended Use

PawPal+ is designed for first-time dog and cat owners who need accessible, personalized guidance on feeding, training, and basic health care. The system is not a substitute for veterinary advice. Every response that touches on health topics includes a recommendation to consult a veterinarian for personalized guidance.

---

## Limitations and Biases

**Retrieval limitations**
The keyword-based retriever selects one file per query. If a question spans multiple topics (for example, "what should I feed my puppy after vaccinations") it will retrieve only the nutrition file and miss the health context. A vector embedding retriever would handle multi-topic questions better.

**Breed bias**
The knowledge base contains general puppy and kitten guidance but does not have breed-specific files beyond what is mentioned in the general nutrition and health files. A Golden Retriever and a Chihuahua will receive the same base advice even though their nutritional needs differ significantly.

**Age approximation**
The system uses age in years and months from the pet profile but does not dynamically adjust recommendations as the pet ages. A user who set up the profile at 3 months will receive the same 3-month advice six months later unless they update the profile.

**Single knowledge base language**
All knowledge base files are in English. Non-English speakers receive English responses regardless of their input language.

**No medical diagnosis**
The system cannot diagnose illness. Questions about symptoms are answered with general warning signs from the knowledge base, which may not apply to the specific pet's situation.

---

## Misuse Prevention

The system prompt instructs the model to use only the retrieved knowledge base context and to acknowledge when it does not have enough information rather than fabricating answers. The prompt explicitly prohibits making up facts.

The `/api/ai/ask` endpoint rejects empty questions with a 400 error before they reach the LLM. API failures return a graceful fallback message rather than exposing error details to the frontend.

The knowledge base is read-only and cannot be modified through the API. There is no user-generated content that could inject malicious context into the retrieval pipeline.

---

## Testing Results

The test harness (`backend/tests/test_harness.py`) ran 6 queries covering nutrition, training, and health for both dogs and cats.

| Test | Question | Status | Confidence | Source |
|---|---|---|---|---|
| 1 | How much should I feed my puppy? | PASS | 60% | Puppy Nutrition |
| 2 | How do I start potty training? | PASS | 67% | Puppy Training |
| 3 | What vaccinations does my puppy need? | PASS | 60% | Puppy Nutrition |
| 4 | How often should I feed my kitten? | PASS | 60% | Kitten Nutrition |
| 5 | How do I set up a litter box? | PASS | 95% | Kitten Training |
| 6 | What are signs my kitten is sick? | PASS | 95% | Kitten Health |

**6 of 6 tests passed. Average confidence: 73%.**

Test 3 retrieved from the nutrition file instead of the health file. The question "what vaccinations does my puppy need" did not contain strong health keywords (the word "vaccinations" was not in the health keyword list). This was identified as a gap and the keyword list was updated after testing to include "vaccine" and "vaccination" as health keywords.

---

## AI Collaboration Reflection

**One instance where AI gave a helpful suggestion**
When building the RAG retriever, the AI suggested using a keyword scoring system that assigns a score to each knowledge base file based on how many topic keywords appear in the question, then picks the highest-scoring file. This was better than my initial idea of just matching the first keyword found, because it handles questions that mention multiple topics by selecting the file with the most relevance signal overall.

**One instance where AI gave a flawed suggestion**
When setting up the Gemini API integration, the AI suggested using the `google.generativeai` package. This package is deprecated and the correct package is `google.genai`. The AI did not flag this issue and the deprecated import produced a FutureWarning on startup. After switching to `google.genai` the quota on the free tier was also exhausted, which the AI did not anticipate. Switching to OpenAI GPT-4o-mini resolved both issues but required rewriting the service layer.

---

## Responsible AI Statement

PawPal+ is a learning tool, not a medical authority. All health-related responses encourage users to consult a licensed veterinarian before making care decisions. The system is transparent about its confidence level on every response, which helps users calibrate how much weight to give each answer. Low confidence responses (below 70%) signal that the retrieved context may not fully address the question.