from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.test_project.crew import TestProject
import uvicorn

app = FastAPI()

class UserDetails(BaseModel):
    name: str
    age: int
    gender: str
    occupation: str

class ChatRequest(BaseModel):
    user_message: str
    history: str
    user_details: UserDetails

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    # Process the chat request using TestProject
    inputs = {
        "user_message": request.user_message,
        "history": request.history,
        "user_details": {
            "name": request.user_details.name,
            "age": request.user_details.age,
            "gender": request.user_details.gender,
            "occupation": request.user_details.occupation,
        },
    }
    try:
        response = TestProject().crew().kickoff(inputs=inputs)
        # Extract the raw response as a string
        if hasattr(response, 'raw'):
            response_text = response.raw
        else:
            response_text = str(response)

        return ChatResponse(response=response_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)