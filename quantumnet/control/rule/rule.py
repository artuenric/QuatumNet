from abc import ABC, abstractmethod
from quantumnet.objects import time

class Rule(ABC):
    def __init__(self, rule_name, ttl):
        self.rule_name = rule_name
        self.actions = {}
        self.host = None
        self.route = []
        self._creations_time = time.get_current_time()
        self.ttl = ttl
        self.age = 0
        self.hit_count = 0
        self.opened = True
        
    def __repr__(self):
        return f"{self.rule_name}"
    
    def set_host(self, host):
        """
        Define o host da regra.
        
        Args:
            host (Host): Host da regra.
        """
        self.host = host
    
    def increment_age(self):
        """Incrementa a idade da regra."""
        self.age += 1
    
    def close(self):
        """Fecha a regra."""
        self.opened = False
        self.host.remove_flow_by_rule(self)
        
    def update_time(self):
        """Atualiza o tempo da regra."""
        # Incrementa a idade
        self.increment_age()
        # Verifica se a regra deve ser fechada
        if self.age == self.ttl:
            # Verifica se a regra foi utilizada
            if self.hit_count > 0:
                # Reinicia a contagem de hits
                self.hit_count = 0
                self.age = self.ttl//2
            else:
                self.close()
    
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