import numpy as np

def compute_weights(metrics, q=0.0, lambda_a=0.0, eps=1e-6):
    losses = np.array([1-m['acc'] for m in metrics])
    gaps = np.array([m['dp']+m['eo'] for m in metrics]) + eps
    base = losses**q / gaps
    if base.sum() == 0:
        base = np.ones_like(base)
    weights = base / base.sum()
    if lambda_a > 0:
        afl = np.zeros_like(weights)
        worst = losses.argmax()
        afl[worst] = 1.0
        weights = (1-lambda_a)*weights + lambda_a*afl
    return weights.tolist()
