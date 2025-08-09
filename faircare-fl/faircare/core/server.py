import torch
from .utils import get_device
from ..fairness.global_stats import aggregate_confusion
from ..algos.aggregator import compute_weights

class Server:
    def __init__(self, model, clients, q=0.0, beta=0.0, lambda_a=0.0):
        self.model = model
        self.clients = clients
        self.q = q
        self.beta = beta
        self.lambda_a = lambda_a
        self.momentum = {k: torch.zeros_like(v) for k, v in model.state_dict().items()}
        self.device = get_device()
        self.model.to(self.device)

    def train_round(self):
        base_state = {k: v.clone() for k, v in self.model.state_dict().items()}
        updates, metrics = [], []
        for c in self.clients:
            c.model.load_state_dict(base_state)
            new_state = c.train()
            delta = {k: new_state[k] - base_state[k] for k in base_state}
            updates.append(delta)
            metrics.append(c.evaluate())
        weights = compute_weights(metrics, q=self.q, lambda_a=self.lambda_a)
        agg = {k: torch.zeros_like(v) for k, v in base_state.items()}
        for w, delta in zip(weights, updates):
            for k in agg:
                agg[k] += w * delta[k]
        if self.beta > 0:
            for k in agg:
                self.momentum[k] = self.beta * self.momentum[k] + (1 - self.beta) * agg[k]
                base_state[k] += self.momentum[k]
        else:
            for k in agg:
                base_state[k] += agg[k]
        self.model.load_state_dict(base_state)
        conf = aggregate_confusion([m['confusion'] for m in metrics])
        return metrics, conf
