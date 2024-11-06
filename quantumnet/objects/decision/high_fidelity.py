from .decision import Decision
class HighFidelity(Decision):
    def __init__(self):
        name = "High Fidelity"
        description = "If the request has a high fidelity"
        super().__init__(name, description)
        
    def __repr__(self):
        return f"{self.name}"
    
    def verify(self, request):
        if request[2] >= 0.9:
            return True
        return False