import exercise.chat.chat as m

def test_chat():
    res = m.chat({})
    assert res["output"] == "chat"
