from pqi.scorer import score_prompt

def test_empty():
    r = score_prompt("")
    assert r["score"] == 0

def test_transcendent():
    r = score_prompt("I wonder: what if every prompt were a moral act shaping shared consciousness?")
    assert r["score"] >= 80
