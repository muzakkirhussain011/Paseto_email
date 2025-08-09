from ..core.server import Server

class FedProx(Server):
    def __init__(self, model, clients, mu=0.0):
        super().__init__(model, clients)
        self.mu = mu
