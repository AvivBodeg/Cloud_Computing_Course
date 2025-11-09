from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import pet_types, pets, pictures

app = FastAPI(
    title="Pet Store API",
    description="A REST API for managing pet store inventory",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(pet_types.router)
app.include_router(pets.router)
app.include_router(pictures.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Pet Store API"}