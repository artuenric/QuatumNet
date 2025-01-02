from .rule import Rule
from ..action import CreateEPRAction, SwapAction

class BasicRuleProactive(Rule):
    def __init__(self, route, controller):
        super().__init__("BasicRuleProactive", controller.default_ttl)  
        self.controller = controller
        self.route = route
        self.behavior()
    
    def behavior(self):
        """Define as ações necessárias para a rota."""
        self.actions = {}  # Inicializa o dicionário de ações
        
        # Tempo 1: Criar pares EPR entre links físicos
        self.actions[1] = self._define_epr_creation()
        
        # Tempo 2+: Realizar entanglement swapping até alcançar fim a fim
        self._define_swapping()
    
    def _define_epr_creation(self):
        """Retorna as ações de criação de pares EPR no tempo 1."""
        actions = []
        for i in range(len(self.route) - 1):
            u, v = self.route[i], self.route[i + 1]
            edge = self.controller.network.edges[u, v]
            
            # Ignorar links virtuais
            if edge.get('virtual_link', False):
                continue
            
            # Criar EPR
            actions.append(CreateEPRAction(u, v, self.controller))
        return actions

    def _define_swapping(self):
        """Define as ações de entanglement swapping."""
        current_time = 2
        remaining_route = self.route[:]
        
        # Enquanto houver mais de dois nós na rota
        while len(remaining_route) > 2:
            self.actions[current_time] = []

            # Adicionar swaps para pares consecutivos
            for i in range(1, len(remaining_route) - 1, 2):
                a = remaining_route[i - 1]  # Nó anterior
                m = remaining_route[i]      # Nó intermediário
                b = remaining_route[i + 1]  # Nó seguinte
                self.actions[current_time].append(SwapAction(a, b, m, self.controller))

            # Atualizar a rota reduzindo intermediários
            remaining_route = [remaining_route[i] for i in range(0, len(remaining_route), 2)]
            current_time += 1
    