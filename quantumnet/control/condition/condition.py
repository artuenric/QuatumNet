from abc import ABC, abstractmethod

class Condition(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def __repr__(self):
        pass
    
    @abstractmethod
    def verify(self, request):
        """
        Verifica se a regra é válida de acordo com as informações da request.

        Args:
            request (Request): Requisição que contém as informações da comunicação.
        """
        pass