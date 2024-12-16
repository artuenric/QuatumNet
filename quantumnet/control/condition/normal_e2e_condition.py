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
        if type(request.alice) == int and type(request.bob) == int:
            if request.fmin > 0 and request.neprs > 0:
                return True
        return False