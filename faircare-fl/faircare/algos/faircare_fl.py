from ..core.server import Server

class FairCare(Server):
    def __init__(self, model, clients, q=0.5, beta=0.0, lambda_a=0.0):
        super().__init__(model, clients, q=q, beta=beta, lambda_a=lambda_a)
