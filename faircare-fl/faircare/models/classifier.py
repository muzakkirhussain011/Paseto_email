import torch
from torch import nn

class MLP(nn.Module):
    def __init__(self, input_dim, hidden=32):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, 1)
        )
        self.output_dim = 1

    def forward(self, x):
        return self.net(x).squeeze(-1)
