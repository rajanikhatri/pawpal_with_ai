import requests
import json

API_BASE = "http://localhost:8000/api"

BASE_PROFILE = {
  "petType": "Dog",
  "petName": "Buddy",
  "ageYears": 0,
  "ageMonths": 3,
  "breed": "Golden Retriever",
  "sex": "Male",
  "source": "Adopted",
  "role": "Family member",
  "commandsKnown": ["Sit"],
  "struggles": ["Potty training"]
}

TEST_CASES = [
  {
    "id": 1,
    "question": "How much should I feed my puppy?",
    "expected_topic": "nutrition",
    "profile": BASE_PROFILE,
  },
  {
    "id": 2,
    "question": "How do I start potty training?",
    "expected_topic": "training",
    "profile": BASE_PROFILE,
  },
  {
    "id": 3,
    "question": "What vaccinations does my puppy need?",
    "expected_topic": "health",
    "profile": BASE_PROFILE,
  },
  {
    "id": 4,
    "question": "How often should I feed my kitten?",
    "expected_topic": "nutrition",
    "profile": {**BASE_PROFILE, "petType": "Cat", "petName": "Luna"},
  },
  {
    "id": 5,
    "question": "How do I set up a litter box?",
    "expected_topic": "training",
    "profile": {**BASE_PROFILE, "petType": "Cat", "petName": "Luna"},
  },
  {
    "id": 6,
    "question": "What are signs my kitten is sick?",
    "expected_topic": "health",
    "profile": {**BASE_PROFILE, "petType": "Cat", "petName": "Luna"},
  },
]

def run_tests():
  print("PawPal+ AI Test Harness")
  print("=" * 50)

  passed = 0
  failed = 0
  results = []

  for test in TEST_CASES:
    try:
      response = requests.post(
        f"{API_BASE}/ai/ask",
        json={
          "question": test["question"],
          "petProfile": test["profile"],
        },
        timeout=30,
      )

      data = response.json()
      answer = data.get("answer", "")
      confidence = data.get("confidence", 0)
      source = data.get("source", "")

      # Pass criteria: answer is non-empty,
      # not an error message, confidence > 0
      is_pass = (
        len(answer) > 20
        and confidence > 0
        and "trouble connecting" not in answer.lower()
      )

      status = "PASS" if is_pass else "FAIL"
      if is_pass:
        passed += 1
      else:
        failed += 1

      results.append({
        "id": test["id"],
        "status": status,
        "confidence": round(confidence * 100),
        "source": source,
        "question": test["question"],
        "answer_preview": answer[:80] + "..." if len(answer) > 80 else answer,
      })

    except Exception as e:
      failed += 1
      results.append({
        "id": test["id"],
        "status": "FAIL",
        "confidence": 0,
        "source": "error",
        "question": test["question"],
        "answer_preview": str(e),
      })

  # Print results
  for result in results:
    print(f"\nTest {result['id']}: {result['status']}")
    print(f"  Question: {result['question']}")
    print(f"  Confidence: {result['confidence']}%")
    print(f"  Source: {result['source']}")
    print(f"  Answer: {result['answer_preview']}")

  print("\n" + "=" * 50)
  print(f"Results: {passed} passed, {failed} failed out of {len(TEST_CASES)} tests")
  avg_confidence = sum(r['confidence'] for r in results) / len(results)
  print(f"Average confidence: {round(avg_confidence)}%")

  if passed == len(TEST_CASES):
    print("All tests passed.")
  else:
    print(f"{failed} test(s) need attention.")

if __name__ == "__main__":
  run_tests()
