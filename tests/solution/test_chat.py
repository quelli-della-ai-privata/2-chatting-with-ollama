import sys 
sys.path.append("packages/solution/chat")
import chat

def test_chat():
    # no args
    args = {}
    res = chat.chat(args)
    assert res["output"].find("llama") != -1

    args = {"input": "What is the capital of Italy, in English?"}
    res = chat.chat(args)
    assert res["output"].find("Rome") != -1
