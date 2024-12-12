from abc import ABC, abstractmethod
class Rule(ABC):
    def __init__(self, rule_name):
        self.rule_name = rule_name
        self.actions = {}
        self.route = []
    
    def __repr__(self):
        return f"{self.rule_name}"
    
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
    