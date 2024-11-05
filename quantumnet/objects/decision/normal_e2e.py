from .decision import Decision
class NormalE2E(Decision):
    def __init__(self):
        self.description = "Normal request E2E"
    
    def verify(self, request):
        """
        Verifica se a request é uma request normal.
        """
        print("Verificando se a request é uma request normal E2E.")
        if all(type(r) == int or type(r) == float for r in request):
            print("Request é uma request normal E2E.")
            if all(r > 0 for r in request[2:]):
                print("Request é com certeza uma request normal E2E.")
                return True
        return False