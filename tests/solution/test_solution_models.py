import solution.models.models as m

def test_models():
    args = {}
    res = m.models(args)
    assert res["output"].find("llama") != -1
