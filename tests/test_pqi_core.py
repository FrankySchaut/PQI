from pqi import PQI, PQIWeights


def test_weights_sum_validation_ok():
    PQIWeights(0.3, 0.4, 0.3).validate()


def test_weights_sum_validation_raises():
    try:
        PQIWeights(0.5, 0.5, 0.2).validate()
    except ValueError:
        return
    raise AssertionError("Expected ValueError for invalid weight sum")


def test_score_monotonic_in_grip():
    pqi = PQI(PQIWeights(0.3, 0.4, 0.3))
    x1 = {"salience": 0.7, "grip": 0.2, "coherence": 0.7}
    x2 = {"salience": 0.7, "grip": 0.8, "coherence": 0.7}
    assert pqi.score(x2) > pqi.score(x1)


def test_score_bounds_and_clamping():
    pqi = PQI()
    x = {"salience": 2.0, "grip": -1.0, "coherence": 0.5}
    s = pqi.score(x)
    assert 0.0 <= s <= 1.0


def test_emily_filter_threshold():
    pqi = PQI(waffle_threshold=0.6)
    low = {"salience": 0.9, "grip": 0.05, "coherence": 0.1}
    high = {"salience": 0.85, "grip": 0.75, "coherence": 0.8}
    assert pqi.emily_filter(low) == "WAFFLE"
    assert pqi.emily_filter(high) == "NOT_WAFFLE"
