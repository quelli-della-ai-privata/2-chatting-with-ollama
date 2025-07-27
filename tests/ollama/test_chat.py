import sys 
sys.path.append("packages/ollama/chat")
import chat

def test_chat():
    res = chat.chat({})
    assert res["output"] == "chat"
