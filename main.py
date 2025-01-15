from fastapi import FastAPI, Depends
import random
import logging
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
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
    "Sure! How can I assist you?",
    "I'm here to help you with any questions!",
    "This is a test response from the AI assistant.",
]

def get_ai_response(user_message: str) -> str:
    logger.info(f"Generating AI response for message: {user_message}")
    # Example: Integrate Datadog
    # Datadog API endpoint: Send logs here.
    return random.choice(DUMMY_RESPONSES)

@app.get("/")
async def home():
    logger.info("Accessed the home endpoint")
    return {"message": "Welcome to the Chat Application!"}

@app.post("/chat/message")
async def send_message(message: dict, db: Session = Depends(get_db)):
    user_message = message.get("message")
    logger.info(f"Received user message: {user_message}")

    ai_response = get_ai_response(user_message)
    logger.info(f"AI response generated: {ai_response}")

    # Check if the message already exists in the database
    existing_message = db.query(ChatMessage).filter(ChatMessage.user == "User", ChatMessage.message == user_message).first()
    if existing_message:
        logger.info(f"Message already exists: {user_message}")
        return {"response": ai_response}

    # Log saved messages
    logger.info(f"Saving user message to database: {user_message}")
    logger.info(f"Saving AI response to database: {ai_response}")

    # Save messages to the database
    db.add(ChatMessage(user="User", message=user_message))
    db.add(ChatMessage(user="AI", message=ai_response))
    db.commit()

    logger.info(f"Messages saved successfully to database.")
    
    return {"response": ai_response}

@app.get("/chat/history")
async def get_history(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    logger.info(f"Accessing chat history from database. Skipping {skip} messages and limiting to {limit}.")
    messages = db.query(ChatMessage).offset(skip).limit(limit).all()
    
    logger.info(f"Retrieved {len(messages)} messages from the database.")
    return {"history": [{"user": msg.user, "message": msg.message} for msg in messages]}

# Placeholder: Logs can be sent to Datadog or Splunk via their APIs.
# Example: 
# logger.info("Sending logs to Datadog API")

# For testing purposes: Ensure consistent AI response for testing
def test_ai_response():
    response = get_ai_response("Hello")
    assert response in [
        "Sure! How can I assist you?",
        "I'm here to help you with any questions!",
        "This is a test response from the AI assistant.",
        "Let me know what you need."
    ]
