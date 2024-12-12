from .rule import Rule
from ..action import CreateEPRAction

class HighFidelityRule(Rule):
    def __init__(self, route, controller):
        super().__init__("HighFidelityRoule")
        self.controller = controller
        
    def behavior(self):
        # Criar EPR entre os hosts da rota
        self.actions[1] = []
        for i in range(len(self.route)):
            self.actions[1].append(CreateEPRAction(self.route[i], self.route[i+1], self.controller))
        
        self.actions[2] = []
        
    
    def prepare(self, controller):
        pass
    
    def run(self):
        pass