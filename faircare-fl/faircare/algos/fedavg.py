from ..core.server import Server

class FedAvg(Server):
    def __init__(self, model, clients):
        super().__init__(model, clients)
