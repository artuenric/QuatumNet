from .rule import Rule
from ..action import CreateEPRAction, SwapAction

class BasicRule(Rule):
    def __init__(self, request, route, controller):
        super().__init__("BasicRule")  # Corrigido nome da regra
        self.controller = controller
        self.route = route
        self.behavior()  # Define as ações
    
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
            
            # Criar EPR se não existirem pares
            if 'eprs' not in edge or len(edge['eprs']) == 0:
                actions.append(CreateEPRAction(u, v, self.controller))
        return actions

    def _define_swapping(self):
        """Define as ações de entanglement swapping."""
        current_time = 2
        remaining_route = self.route[:]
        
        while len(remaining_route) > 2:  # Enquanto houver mais de dois nós na rota
            self.actions[current_time] = []
            
            # Adicionar swaps para pares consecutivos
            for a, m, b in zip(remaining_route, remaining_route[1:], remaining_route[2:]):
                self.actions[current_time].append(SwapAction(a, b, m, self.controller))
            
            # Atualizar a rota para pares reduzidos (simulação de fim-a-fim)
            remaining_route = remaining_route[::2]
            current_time += 1
    
    def run(self):
        """Executa as ações no tempo certo."""
        for time in sorted(self.actions.keys()):
            print(f"Tempo: {time}")
            for action in self.actions[time]:
                print(f"Executando ação: {action}")
                action.run()