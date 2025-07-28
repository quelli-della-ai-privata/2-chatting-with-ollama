import solution.chat.chat as m

def test_chat():
    # no args
    args = {}
    res = m.chat(args)
    assert res["output"].find("llama") != -1

    args = {"input": "What is the capital of Italy, in English?"}
    res = m.chat(args)
    assert res["output"].find("Rome") != -1
