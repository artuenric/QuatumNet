class Request():
    """
    Representa uma requisição feita por um host.
    """
    def __init__(self, alice, bob, fmin, neprs):
        self.alice = alice
        self.bob = bob
        self.fmin = fmin
        self.neprs = neprs
        self.id = self.set_id()
        self.open = True
        self.starttime = 0
        self.endtime = 0
    
    def __repr__(self):
        return self.id
    
    def set_id(self):
        return f"R{hex(id(self))[-6:].upper()}:{self.alice}-{self.bob}:{self.fmin}:{self.neprs}"
    
    def close(self, endtime):
        """
        Fecha a requisição.
        """
        self.endtime = endtime
        self.open = False
    