from .rule import Rule
from ..action import CreateEPRAction, SwapAction

class BasicRule(Rule):
    def __init__(self, request, route, controller):
        super().__init__("BasicRoule")
        self.controller = controller
        self.route = route
        self.behavior()
        
    def behavior(self):
        # Criar EPR entre os hosts da rota
        self.actions[1] = []
        for i in range(len(self.route)-1):
            if self.controller.network.edges[self.route[i], self.route[i+1]]['virtual_link'] == True:
                # Se a aresta for virtual, ignorar
                continue
            if len(self.controller.network.edges[self.route[i], self.route[i+1]]['eprs']) == 0:
                # Se não houver pares epr, criar
                self.actions[1].append(CreateEPRAction(self.route[i], self.route[i+1], self.controller))
        
        # Swap entre os pares EPR do caminho
        self.actions[2] = []
        for a, m, b in zip(self.route, self.route[1:], self.route[2:]):
           self.actions[2].append(SwapAction(a, b, m, self.controller))
    
    def run(self):
        for time in self.actions:
            print("Tempo:", time)
            for a in self.actions[time]:
                print("Executando ação:", a)
                a.run()