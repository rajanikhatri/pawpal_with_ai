# PawPal+ AI

An AI-powered pet care assistant for first-time dog and cat owners. PawPal+ uses Retrieval-Augmented Generation (RAG) with OpenAI GPT-4o-mini to deliver personalized, knowledge-grounded care advice based on each pet's profile.

**Live Demo:** [Add Vercel URL here]
**Video Walkthrough:** [Add Loom URL here]



## Base Project

This project extends the original PawPal+ (Module 1-3 submission), a Python OOP pet management system built with Streamlit. The original system supported task scheduling, recurring task logic, conflict detection, and a single-owner dashboard. This version rebuilds the frontend in React, replaces the Streamlit UI with a FastAPI backend, and adds a full AI layer using RAG, confidence scoring, interaction logging, and a test harness.

---

## What It Does

PawPal+ guides first-time pet owners through everything they need to know in one place. A user creates a pet profile during onboarding (species, breed, age, struggles, training goals), and the app uses that profile to personalize every AI response. The AI assistant answers questions about feeding, training, health, and behavior using a curated veterinary knowledge base rather than general internet knowledge.

---

## Architecture Overview

```
User (React Frontend)
        |
        | HTTP POST with question + pet profile
        v
FastAPI Backend (port 8000)
        |
   +----|----+
   |         |
   v         v
RAG          Logger Service
Retriever    (records every interaction)
   |
   | Keyword search on 6 knowledge base files
   v
Retrieved Context + Pet Profile + Question
   |
   v
OpenAI GPT-4o-mini
   |
   v
Answer + Confidence Score
   |
   v
React Frontend renders response + confidence badge
```

The RAG retriever uses keyword matching to select the most relevant knowledge base file (nutrition, training, or health) for the pet type (dog or cat) before sending anything to the LLM. This means the model answers from grounded context rather than general training data.

---

## Setup Instructions

### Prerequisites
- Node.js 18+
- Python 3.11+
- OpenAI API key

### Backend

```bash
cd backend
python3 -m pip install -r requirements.txt --break-system-packages
```

Create `backend/.env`:
```
OPENAI_API_KEY=your_openai_key_here
```

Start the server:
```bash
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` in your browser.

---

## Sample Interactions

**Input 1**
```
Question: How much should I feed my puppy?
Pet: Buddy, 3-month-old Golden Retriever
```
**Output:**
```
For Buddy at 3 months old, you should feed him about 350-500 kcal 
per day divided into 4 small meals. Make sure to choose a puppy food 
labeled complete and balanced for growth with at least 22.5% protein. 
A practical next step is to check the food label for specific feeding 
guidelines based on Buddy's weight.

Confidence: 60% · Puppy Nutrition
```

**Input 2**
```
Question: How do I start potty training?
Pet: Buddy, 3-month-old Golden Retriever
```
**Output:**
```
To start potty training Buddy, take him outside first thing in the 
morning and last thing at night. At 3 months, he needs a potty break 
about every 1-2 hours while awake. Always reward him immediately after 
he goes outside. A practical next step is to pick one consistent outdoor 
spot so the smell cues help him learn faster.

Confidence: 67% · Puppy Training
```

**Input 3**
```
Question: How do I set up a litter box?
Pet: Luna, 3-month-old Cat
```
**Output:**
```
To set up a litter box for Luna, choose a low-sided box so she can 
easily climb in. Place it in a quiet location away from her food and 
water but close enough to find. Use unscented soft litter and put her 
in it after meals, naps, and play. Keep it clean every day. A practical 
next step is to praise her calmly after successful use.

Confidence: 95% · Kitten Training
```

---

## Design Decisions

**Why RAG instead of direct prompting**
Sending questions directly to GPT-4o-mini without context produces generic answers that do not account for the pet's age, breed, or specific struggles. RAG forces the model to answer from vetted veterinary sources, which makes responses more reliable and trustworthy for first-time owners who may act on the advice.

**Why keyword-based retrieval instead of vector embeddings**
For a knowledge base of 6 files, vector embeddings add significant infrastructure complexity (embedding model, vector database) with minimal retrieval benefit. Keyword matching against 6 well-named files is fast, deterministic, and easy to debug. The tradeoff is that it handles synonyms less gracefully, which is documented as a known limitation.

**Why OpenAI GPT-4o-mini**
The free Gemini API quota was exhausted during development. GPT-4o-mini provides high quality output at very low cost (fractions of a cent per call) and has a stable, well-documented Python SDK.

**Why localStorage instead of Supabase for the submission**
Supabase integration was planned but deprioritized to meet the submission deadline. localStorage keeps the demo fast and self-contained. All database schema and Supabase integration code is documented in PLAN.md for the next iteration.

---

## Testing Summary

The test harness at `backend/tests/test_harness.py` runs 6 queries against the live API and reports pass/fail with confidence scores.

```
Results: 6 passed, 0 failed out of 6 tests
Average confidence: 73%
All tests passed.
```

Test 3 (vaccinations) retrieved from the nutrition file instead of the health file because the question did not contain strong health keywords. This is a known limitation of keyword-based retrieval and is addressed in the reflection below.

The system handled all error cases correctly: empty inputs return a 400 error, API failures return a graceful fallback message, and confidence scores are always included in every response.

---

## Reflection

Building this project clarified how much of RAG quality depends on retrieval design rather than the LLM itself. The model consistently produced accurate, personalized answers when the right context was retrieved, and appropriately hedged when it was not. The most surprising finding was that confidence scores based on keyword overlap between the question and retrieved context correlated reasonably well with actual answer quality, even though the scoring method is simple.

The biggest limitation is the keyword retrieval system. A question like "does my puppy need shots" would retrieve the nutrition file because "puppy" scores higher than "shots" does against the health file keywords. A vector embedding approach would handle this correctly. This is the first improvement planned for the next iteration.

---

## Coming Soon

- Owner calendar with schedule conflict detection
- Vet expense tracker
- Food recall notifications
- Supabase database for persistent multi-pet storage
- Household sharing for multiple users
