from main import get_ai_response

def test_ai_response():
    response = get_ai_response("Hello")
    assert response in [
        "Sure! How can I assist you?",
        "I'm here to help you with any questions!",
        "This is a test response from the AI assistant.",
    ]


