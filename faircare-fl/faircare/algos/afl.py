from ..core.server import Server

class AFL(Server):
    def __init__(self, model, clients, lambda_a=1.0):
        super().__init__(model, clients, lambda_a=lambda_a)
