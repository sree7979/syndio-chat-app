from main import get_ai_response

def test_ai_response():
    response = get_ai_response("Hello")
    assert response in [
        "Hi there! I'm a simulated AI assistant.",
        "Hello! This is a placeholder AI response.",
        "I'm just a dummy function pretending to be AI.",
    ]

