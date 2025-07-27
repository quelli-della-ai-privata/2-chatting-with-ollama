import sys 
sys.path.append("packages/ollama/models")
import models

def test_models():
    res = models.models({})
    assert res["output"] == "models"
