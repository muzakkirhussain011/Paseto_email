from ..core.server import Server

class QFFL(Server):
    def __init__(self, model, clients, q=1.0):
        super().__init__(model, clients, q=q)
