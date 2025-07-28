import os, requests as req
def test_chat():
    url = os.environ.get("OPSDEV_HOST", "") + "/api/my/exercise/chat"
    res = req.get(url).json()
    assert res.get("output") == "chat"
