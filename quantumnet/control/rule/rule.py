from abc import ABC, abstractmethod
 
class Rule(ABC):
    def __init__(self, rule_name, ttl):
        self.rule_name = rule_name
        self.actions = {}
        self.route = []
        self.ttl = ttl
        self.age = 0
        self.hit_count = 0
        
    def __repr__(self):
        return f"{self.rule_name}"
    
    def increment_age(self):
        """Incrementa a idade da regra."""
        self.age += 1
    
    def decrement_ttl(self):
        """Decrementa o TTL da regra."""
        self.ttl -= 1
    
    def run(self):
        """Executa as ações no tempo certo."""
        # Regra executada
        self.hit_count += 1
        for time in sorted(self.actions.keys()):
            print(f"[{self.__repr__()}] Passo: {time}")
            for action in self.actions[time]:
                print(f"[{self.__repr__()}] Ação: {action}")
                action.run()
    
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