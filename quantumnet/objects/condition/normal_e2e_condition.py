from .condition import Condition

class NormalE2ECondition(Condition):
    def __init__(self):
        name = "Normal E2E"
        description = "If the request is a normal E2E request."
        super().__init__(name, description)
    
    def __repr__(self):
        return f"{self.name}"
    
    def verify(self, request):
        """
        Verifica se a request é uma request normal.
        """

        if all(type(r) == int or type(r) == float for r in request):
            if all(r > 0 for r in request[2:]):
                return True
        return False