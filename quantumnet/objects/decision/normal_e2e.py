from .decision import Decision
class NormalE2E(Decision):
    def __init__(self):
        self.description = "Normal request E2E"
    
    def verify(self, request):
        """
        Verifica se a request é uma request normal.
        """
        if all(type(r) == int for r in request):
            if all(r > 0 for r in request[:2]):
                return True
        return False