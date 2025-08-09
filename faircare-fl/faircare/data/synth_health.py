import numpy as np
import torch
from torch.utils.data import DataLoader, TensorDataset


def generate_synth(n=1000, n_features=10, seed=0):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, n_features))
    s = rng.integers(0, 2, size=n)
    logits = X[:, 0] + 0.5 * s
    probs = 1 / (1 + np.exp(-logits))
    y = rng.binomial(1, probs)
    ds = TensorDataset(torch.tensor(X, dtype=torch.float32), torch.tensor(y, dtype=torch.float32), torch.tensor(s, dtype=torch.float32))
    return DataLoader(ds, batch_size=32, shuffle=True)
