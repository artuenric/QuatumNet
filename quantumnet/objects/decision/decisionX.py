from .decision import Decision
class Decision_X(Decision):
    def __init__(self):
        name = "Decision X"
        description = "Se o destino for 0"
        super().__init__(name, description)

    def verify(self, request: list):
        """
        Verifica se a regra é válida de acordo com as informações da request.
        """
        # O destino é o segundo item da request.
        if request[1] == 0:
            return True
        return False