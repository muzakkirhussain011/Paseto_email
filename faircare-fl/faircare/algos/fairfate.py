from ..core.server import Server

class FairFATE(Server):
    def __init__(self, model, clients, beta=0.9):
        super().__init__(model, clients, beta=beta)
