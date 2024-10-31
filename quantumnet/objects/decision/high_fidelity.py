from .decision import Decision
class HighFidelity(Decision):
    def __init__(self):
        self.description = "High Fidelity"
        
    def verify(self, request):
        if request[2] >= 0.9:
            return True
        return False