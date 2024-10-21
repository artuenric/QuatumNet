from abc import ABC, abstractmethod

class Roule(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def __str__(self):
        return f"Roule: {self.name} - {self.description}"
    
    @abstractmethod
    def verify(self, info: list):
        """
        Verifica se a regra é válida de acordo com as informações da request.

        Args:
            info (list): lista de informações que devem ser verificadas do request.
        """
        pass