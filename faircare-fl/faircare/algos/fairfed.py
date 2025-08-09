from ..core.server import Server

class FairFed(Server):
    def __init__(self, model, clients, q=0.0):
        super().__init__(model, clients, q=q)
