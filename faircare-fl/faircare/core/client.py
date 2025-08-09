import torch
from torch import nn, optim
from .utils import get_device
from ..models.adversary import Adversary, grad_reverse

class Client:
    def __init__(self, cid, model, train_loader, val_loader, lambda_g=0.0, use_adversary=True):
        self.id = cid
        self.model = model
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.lambda_g = lambda_g
        self.use_adversary = use_adversary and lambda_g > 0
        if self.use_adversary:
            self.adv = Adversary(model.output_dim)
            self.adv_opt = optim.Adam(self.adv.parameters(), lr=1e-3)
        self.opt = optim.Adam(self.model.parameters(), lr=1e-3)
        self.loss_fn = nn.BCEWithLogitsLoss()
        self.device = get_device()
        self.model.to(self.device)
        if self.use_adversary:
            self.adv.to(self.device)

    def train(self, epochs=1):
        self.model.train()
        for _ in range(epochs):
            for x, y, s in self.train_loader:
                x, y, s = x.to(self.device), y.to(self.device), s.to(self.device)
                if self.use_adversary:
                    # adversary step
                    with torch.no_grad():
                        logits = self.model(x)
                    adv_loss = self.loss_fn(self.adv(logits.detach()), s.float())
                    self.adv_opt.zero_grad()
                    adv_loss.backward()
                    self.adv_opt.step()
                # classifier step
                logits = self.model(x)
                loss = self.loss_fn(logits, y.float())
                if self.use_adversary:
                    adv_pred = self.adv(grad_reverse(logits))
                    fair_loss = self.loss_fn(adv_pred, s.float())
                    loss = loss - self.lambda_g * fair_loss
                self.opt.zero_grad()
                loss.backward()
                self.opt.step()
        return {k: v.clone() for k, v in self.model.state_dict().items()}

    def evaluate(self):
        from .evaluation import evaluate
        return evaluate(self.model, self.val_loader)
