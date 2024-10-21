from .decision import Decision
class Decision_X(Decision):
    def __init__(self):
        name = "Decision X"
        description = "Se o destino for 0, aplicar a ação 0"
        super().__init__(name, description)

    def verify(self, info: list):
        if info[1] == 0:
            return True
        return False