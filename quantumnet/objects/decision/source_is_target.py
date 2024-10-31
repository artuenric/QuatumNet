from .decision import Decision
class SourceIsTarget(Decision):
    def __init__(self):
        name = "Source is Target"
        description = "Se o destino for o mesmo que a origem"
        super().__init__(name, description)

    def verify(self, request: list):
        """
        Verifica se a regra é válida de acordo com as informações da request.
        """
        if request[1] == request[0]:
            return True
        return False