import argparse
import os
import json
from ..data import load_heart, load_adult, dirichlet_partition
from ..models import MLP
from ..core.client import Client
from ..core.server import Server
from ..core.trainer import train
from ..algos import fedavg, faircare_fl
from torch.utils.data import DataLoader, TensorDataset
import torch

def build_clients(X, y, s, num_clients, alpha, batch_size, lambda_g, use_adv, seed):
    parts = dirichlet_partition(len(X), num_clients, alpha, seed)
    clients = []
    for cid, idx in enumerate(parts):
        ds = TensorDataset(torch.tensor(X[idx]), torch.tensor(y[idx]), torch.tensor(s[idx]))
        loader = DataLoader(ds, batch_size=batch_size, shuffle=True)
        client = Client(cid, None, loader, loader, lambda_g=lambda_g, use_adversary=use_adv)
        clients.append(client)
    return clients


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', choices=['heart','adult'], default='heart')
    parser.add_argument('--algo', choices=['fedavg','faircare'], default='faircare')
    parser.add_argument('--num_clients', type=int, default=5)
    parser.add_argument('--rounds', type=int, default=1)
    parser.add_argument('--local_epochs', type=int, default=1)
    parser.add_argument('--batch_size', type=int, default=32)
    parser.add_argument('--lr', type=float, default=1e-3)
    parser.add_argument('--lambdaG', type=float, default=0.0)
    parser.add_argument('--lambdaA', type=float, default=0.0)
    parser.add_argument('--q', type=float, default=0.0)
    parser.add_argument('--beta', type=float, default=0.0)
    parser.add_argument('--dirichlet_alpha', type=float, default=0.5)
    parser.add_argument('--sensitive_attr', default='sex')
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--outdir', default='runs/demo/')
    parser.add_argument('--no-adv', action='store_true')
    args = parser.parse_args()

    if args.dataset == 'heart':
        train_loader, test_loader = load_heart(batch_size=args.batch_size, seed=args.seed)
        X = train_loader.dataset.tensors[0].numpy()
        y = train_loader.dataset.tensors[1].numpy()
        s = train_loader.dataset.tensors[2].numpy()
        input_dim = X.shape[1]
    else:
        train_loader, test_loader = load_adult(batch_size=args.batch_size, seed=args.seed)
        X = train_loader.dataset.tensors[0].numpy()
        y = train_loader.dataset.tensors[1].numpy()
        s = train_loader.dataset.tensors[2].numpy()
        input_dim = X.shape[1]

    clients = []
    parts = dirichlet_partition(len(X), args.num_clients, args.dirichlet_alpha, args.seed)
    for cid, idx in enumerate(parts):
        ds = TensorDataset(torch.tensor(X[idx]), torch.tensor(y[idx]), torch.tensor(s[idx]))
        loader = DataLoader(ds, batch_size=args.batch_size, shuffle=True)
        val_loader = loader
        model = MLP(input_dim)
        client = Client(cid, model, loader, val_loader, lambda_g=args.lambdaG, use_adversary=not args.no_adv)
        clients.append(client)

    global_model = MLP(input_dim)
    if args.algo == 'fedavg':
        server = fedavg.FedAvg(global_model, clients)
    else:
        server = faircare_fl.FairCare(global_model, clients, q=args.q, beta=args.beta, lambda_a=args.lambdaA)

    history = train(server, rounds=args.rounds, outdir=args.outdir, seed=args.seed)
    with open(os.path.join(args.outdir, 'config.json'), 'w') as f:
        json.dump(vars(args), f)

if __name__ == '__main__':
    main()
