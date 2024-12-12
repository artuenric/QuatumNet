class Request():
    """
    Representa uma requisição feita por um host.
    """
    def __init__(self, alice, bob, fmin, neprs):
        self.alice = alice
        self.bob = bob
        self.fmin = fmin
        self.neprs = neprs
        self.open = True
        self.starttime = 0
        self.endtime = 0
        
    def close(self, endtime):
        """
        Fecha a requisição.
        """
        self.endtime = endtime
        self.open = False