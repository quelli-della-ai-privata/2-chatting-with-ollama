import exercise.models.models as m

def test_models():
    args = {}
    res = m.models(args)
    assert res["output"] == "models"
