from fastapi import FastAPI

app = FastAPI(title="PawPal+ API")


@app.get("/")
def read_root():
    return {"message": "Welcome to the PawPal+ API"}
