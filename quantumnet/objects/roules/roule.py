from abc import ABC, abstractmethod
class Roule(ABC):
    def __init__(self, roule_name):
        self.roule_name = roule_name
        self.actions = {}
        self.route = []
    
    def __repr__(self):
        return f"{self.roule_name}"
    
    def set_route(self, route):
        """
        Define a rota da regra.
        
        Args:
            route (list): Lista de nós da rota.
        """
        self.route = route
    
    @abstractmethod
    def behavior(self):
        """
        Define o comportamento da regra.
        """
        pass
    
    @abstractmethod
    def run(self):
        """
        Executa as ações da regra.
        """
        pass
    