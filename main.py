from fastapi import FastAPI, status

app = FastAPI(
    title="DevFlow API Engine",
    version="1.0.0"
)

# Root route returning basic metadata
@app.get("/", status_code=status.HTTP_200_OK)
def read_root():
    return {
        "status": "online",
        "service": "DevFlow API",
        "message": "Welcome to DevFlow Engine!"
    }

# Path Parameter Example: Getting a specific item by ID
@app.get("/items/{item_id}", status_code=status.HTTP_200_OK)
def get_item(item_id: int):
    return {
        "item_id": item_id,
        "type": "Path Parameter Demonstration"
    }

# Query Parameter Example: Filtering/Searching (e.g., /search?q=fastapi)
@app.get("/search", status_code=status.HTTP_200_OK)
def search_items(q: str = "default", limit: int = 10):
    return {
        "query": q,
        "limit": limit,
        "type": "Query Parameter Demonstration"
    }