from .condition import Condition

class HighFidelityCondition(Condition):
    def __init__(self):
        name = "High Fidelity"
        description = "If the request has a high fidelity"
        super().__init__(name, description)
        
    def __repr__(self):
        return f"{self.name}"
    
    def verify(self, request):
        if request.fmin >= 0.9:
            return True
        return False