from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

API_KEY = "devflow-secret-key-2026"
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key. Include 'X-API-Key' in headers."
        )
    return api_key