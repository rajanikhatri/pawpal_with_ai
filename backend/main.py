from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import ai, pets, tasks

app = FastAPI(title="PawPal+ API", version="1.0.0")

app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:5173"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(ai.router, prefix="/api/ai", tags=["AI"])
app.include_router(pets.router, prefix="/api/pets", tags=["Pets"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])

@app.get("/")
def read_root():
  return {"message": "PawPal+ API is running"}

@app.get("/health")
def health_check():
  return {"status": "healthy"}
