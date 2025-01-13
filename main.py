from fastapi import FastAPI
import random
import logging

app = FastAPI()

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ChatApp")

# Dummy AI responses
DUMMY_RESPONSES = [
    "Hi there! I'm a simulated AI assistant.",
    "Hello! This is a placeholder AI response.",
    "I'm just a dummy function pretending to be AI.",
]

chat_history = []

def get_ai_response(user_message: str) -> str:
    logger.info(f"Generating AI response for message: {user_message}")
    # Example: Integrate Datadog
    # Datadog API endpoint: Send logs here.
    return random.choice(DUMMY_RESPONSES)

@app.get("/")
async def home():
    return {"message": "Welcome to the Chat Application!"}

@app.post("/chat/message")
async def send_message(message: dict):
    user_message = message.get("message")
    ai_response = get_ai_response(user_message)
    chat_history.append({"user": "User", "message": user_message})
    chat_history.append({"user": "AI", "message": ai_response})
    return {"response": ai_response}

@app.get("/chat/history")
async def get_history():
    return {"history": chat_history}
