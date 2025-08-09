from ..core.server import Server

class FedGFT(Server):
    def __init__(self, model, clients, lambda_g=1.0):
        for c in clients:
            c.lambda_g = lambda_g
        super().__init__(model, clients)
