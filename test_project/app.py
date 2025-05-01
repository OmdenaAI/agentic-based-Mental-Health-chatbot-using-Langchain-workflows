from fastapi import FastAPI
from pydantic import BaseModel
from src.test_project.crew import TestProject
import uvicorn

app = FastAPI()

class ChatRequest(BaseModel):
    user_message: str
    history: str

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    # Process the chat request using TestProject
    inputs = {
        "user_message": request.user_message,
        "history": request.history
    }
    try:
        response = TestProject().crew().kickoff(inputs=inputs)
    except Exception as e:
        return ChatResponse(response=f"Error: {str(e)}")
    return ChatResponse(response=response)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)