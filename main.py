from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import random
import logging
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session

app = FastAPI()

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger("ChatApp")

# Database setup
DATABASE_URL = "sqlite:///./chat.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, index=True)
    user = Column(String)
    message = Column(String)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dummy AI responses
DUMMY_RESPONSES = [
    "Hi there! I'm a simulated AI assistant.",
    "Hello! This is a placeholder AI response.",
    "I'm just a dummy function pretending to be AI.",
    "Sure! How can I assist you?"
]

def get_ai_response(user_message: str) -> str:
    logger.info(f"Generating AI response for message: {user_message}")
    return random.choice(DUMMY_RESPONSES)

# Input validation model
class ChatMessageRequest(BaseModel):
    user: str
    message: str

@app.get("/")
async def home():
    logger.info("Accessed the home endpoint")
    return {"message": "Welcome to the Chat Application!"}

@app.post("/chat/message")
async def send_message(request: ChatMessageRequest, db: Session = Depends(get_db)):
    try:
        user_message = request.message
        logger.info(f"Received user message from {request.user}: {user_message}")

        # Generate AI response
        ai_response = get_ai_response(user_message)
        logger.info(f"AI response generated: {ai_response}")

        # Check if the message already exists in the database
        existing_message = db.query(ChatMessage).filter(ChatMessage.user == request.user, ChatMessage.message == user_message).first()
        if existing_message:
            logger.info(f"Message already exists: {user_message}")
            return {"response": ai_response}

        # Save messages to the database
        db.add(ChatMessage(user=request.user, message=user_message))
        db.add(ChatMessage(user="AI", message=ai_response))
        db.commit()
        logger.info("Messages saved successfully to database.")
        
        return {"response": ai_response}
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing your message")

@app.get("/chat/history")
async def get_history(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    try:
        logger.info(f"Accessing chat history from database. Skipping {skip} messages and limiting to {limit}.")
        messages = db.query(ChatMessage).offset(skip).limit(limit).all()
        
        logger.info(f"Retrieved {len(messages)} messages from the database.")
        return {"history": [{"user": msg.user, "message": msg.message} for msg in messages]}
    except Exception as e:
        logger.error(f"Error retrieving chat history: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving chat history")


# Placeholder: Logs can be sent to Datadog or Splunk via their APIs.
# Example: 
# logger.info("Sending logs to Datadog API")

# For testing purposes: Ensure consistent AI response for testing

