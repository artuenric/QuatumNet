from .roule import Roule
class X_Roule(Roule):
    def __init__(self):
        name = "X_Roule"
        description = "Se o destino for 0, aplicar a regra 0"
        super().__init__(name, description)

    def verify(self, info: list):
        if info[1] == 0:
            return 0