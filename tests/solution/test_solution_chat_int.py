import os, requests as req
def test_chat():
    url = os.environ.get("OPSDEV_HOST", "") + "/api/my/solution/chat"
    res = req.get(url).json()
    assert res.get("output").find("llama") != -1

    args = {"input": "What is the capital of Italy, in English?"}
    res = req.post(url, json=args).json()
    assert res["output"].find("Rome") != -1
