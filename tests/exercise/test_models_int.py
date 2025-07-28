import os, requests as req
def test_models():
    url = os.environ.get("OPSDEV_HOST") + "/api/my/exercise/models"
    res = req.get(url).json()
    assert res.get("output") == "models"
