import uvicorn
from web_app import app  # Import the FastAPI instance from __init__.py

if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host="localhost", 
        port=8000,
        
    )