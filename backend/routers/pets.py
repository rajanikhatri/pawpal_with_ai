from fastapi import APIRouter
router = APIRouter()

@router.get("/")
def list_pets():
  return {"message": "Pets endpoint - coming in Day 3"}
