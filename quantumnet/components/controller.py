import networkx as nx
from ..components import Network, Host
from ..objects.decision import SourceIsTarget, HighFidelity, NormalE2E
from ..objects.action import DropRequestAction, HighPurificationAction, CreateEPRAction, SwapAction, PurificationAction

class Controller():
    def __init__(self, network):
        self.network = network
        self.hosts = None
        self.links = None
        self.decisions = self.set_decisions()
    
    def calculate_route(self, source, target):
        """
        Calcula a rota para o destino.

        Args:
            source (int): ID do host de origem.
            target (int): ID do host de destino.
        """
        G = self.network.graph
        route = nx.shortest_path(G, source=source, target=target)
        return route
            
    def set_decisions(self):
        """
        Define as decisões do controlador para escolher as ações.
        """
        return {
            (SourceIsTarget(),): [DropRequestAction],            
            (HighFidelity(),): [HighPurificationAction],
            (NormalE2E(),): [CreateEPRAction, SwapAction, PurificationAction],
        }
    
    def apply_decision(self, request):
        """
        Aplica uma decisão do controlador para um match específico. Retorna a ação que deve ser executada.

        Args:
            info (lista): Lista com as informações da request.
        
        Returns:
            actions (lista): Lista com as ações que devem ser executadas.
        """
        
        for decision in self.decisions:
            # Retorna a ação correspondente as decisões da tabela que são válidas para a request.
            if all(d.verify(request) for d in decision):
                print("Decisão aplicada:", decision)
                return self.decisions[decision]

        return [DropRequestAction]
        
    def add_match_route_roule_in_host(self, request, host):
        """
        Adiciona um match, uma rota e ações ao host. Isso é feito após a decisão do controlador e utilizando o método add_match_actions do host.

        Args:
            request (list): Lista com as informações da request.
            host (Host): Host que terá o match, a rota e as ações adicionadas.
        """
        # Obtém as ações que devem ser executadas de acordo com as decisões do controlador.
        actions = self.apply_decision(request)
        # Calcula a rota para o destino (segundo item da lista) da request.
        route = self.calculate_route(request[0], request[1])
        # Qualifica as ações de acordo com as informações da request.
        roule = self.qualify_actions(request, actions, route)
        print("Ações qualificadas:", roule)
        # Adiciona a rota e as ações ao host.
        host.add_match_route_roule(request=request, route=route, roule=roule)

    # Provavelmente o ideal seria um método para cada tipo de ação, mas por enquanto vamos manter assim
    # LITERALMENTE PROTOCOLOS
    def qualify_actions(self, request, actions, route):
        """
        Qualifica uma ação de acordo com as informações da request.

        Args:
            request (list): Lista com as informações da request.
            actions (list): Lista com as ações que devem ser executadas.
            route (list): Lista com a rota para o destino.
        """
        # TODO: Aqui também vai ser considerado o time-slot etc. Essa é uma função ABSURDAMENTE importante uma das mais complexas.
        # TODO: Cada regra deve conter várias ações, provavelmente repetidas, mas com informações diferentes. Por isso, essa parte do código deve ser alterada futuramente. Focando em abstrair o processo.
        
        roule = {}
        
        for action in actions:
            if action == CreateEPRAction:
                paths = [(route[i], route[i+1]) for i in range(len(route) - 1)]
                roule[1] = [CreateEPRAction(path, self) for path in paths]
            elif action == SwapAction:
                pairs = [(route[i], route[i+1]) for i in range(len(route) - 1)]
                roule[2] = [SwapAction(pairs[i], pairs[i+1], self) for i in range(len(pairs) - 1)]
                
        return roule
    
    def run_roule(self, roule):
        """
        Executa as ações de um roule.

        Args:
            roule (dict): Dicionário com as ações que devem ser executadas.
        """
        
        for action in roule:
            action.run()
        