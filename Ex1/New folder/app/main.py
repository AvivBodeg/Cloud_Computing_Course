from fastapi import FastAPI

app = FastAPI(
    title="Pet Store API",
    description="REST API for managing pet store inventory",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Welcome to Pet Store API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)