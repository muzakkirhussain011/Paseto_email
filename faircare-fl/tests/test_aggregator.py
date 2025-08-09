from faircare.algos.aggregator import compute_weights

def test_weights_sum_one():
    metrics = [{'acc':0.8,'dp':0.1,'eo':0.1},{'acc':0.5,'dp':0.2,'eo':0.2}]
    w = compute_weights(metrics, q=0.5)
    assert abs(sum(w)-1) < 1e-6
