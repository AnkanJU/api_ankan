from fastapi import FastAPI

app = FastAPI(
    title="DevFlow API",
    description="Task & Developer Workflow Engine API",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "DevFlow API",
        "message": "Welcome to the DevFlow API Engine!"
    }