import numpy as np


def dirichlet_partition(n, num_clients, alpha=0.5, seed=0):
    rng = np.random.default_rng(seed)
    probs = rng.dirichlet([alpha] * num_clients)
    counts = (probs * n).astype(int)
    counts[-1] += n - counts.sum()
    indices = np.arange(n)
    rng.shuffle(indices)
    parts = []
    start = 0
    for c in counts:
        parts.append(indices[start:start+c])
        start += c
    return parts
