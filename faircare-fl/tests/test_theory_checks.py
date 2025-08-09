from faircare.algos.aggregator import compute_weights

def test_q_weighting_monotonic():
    metrics = [{'acc':0.9,'dp':0.1,'eo':0.1},{'acc':0.5,'dp':0.1,'eo':0.1}]
    w = compute_weights(metrics, q=1.0)
    assert w[1] > w[0]
