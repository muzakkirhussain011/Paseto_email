import json
import os
from .server import Server
from ..fairness.metrics import dp_gap, eo_gap


def train(server: Server, rounds=1, outdir='runs/', seed=0):
    os.makedirs(outdir, exist_ok=True)
    history = []
    for r in range(rounds):
        metrics, conf = server.train_round()
        agg_dp = dp_gap(conf)
        agg_eo = eo_gap(conf)
        acc = sum(m['acc'] for m in metrics) / len(metrics)
        history.append({'round': r, 'acc': acc, 'dp': agg_dp, 'eo': agg_eo})
        print(f"Round {r}: acc={acc:.3f} dp={agg_dp:.3f} eo={agg_eo:.3f}")
    with open(os.path.join(outdir, 'history.json'), 'w') as f:
        json.dump(history, f)
    return history
