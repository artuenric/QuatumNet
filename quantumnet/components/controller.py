import networkx as nx
from ..components import Network, Host
from ..objects.decision import Decision_X
from ..objects.action import CreateEPRAction, SwapAction, PurificationAction

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
        decision = {
            (Decision_X(),): [CreateEPRAction, SwapAction, PurificationAction], # que coisa horrivel
        }
        return decision
    
    def apply_decision(self, request):
        """
        Aplica uma decisão do controlador para um match específico. Retorna a ação que deve ser executada.

        Args:
            info (lista): Lista com as informações da request.
        
        Returns:
            action (lista): Lista com as ações que devem ser executadas.
        """
        
        print("Aplicando decisão do controlador para a request", request)
        action = None
        for decision in self.decisions:
            print("Decisões:", [d.description for d in decision])
            # Retorna a ação correspondente as decisões da tabela que são válidas para a request.
            if all(d.verify(request) for d in decision):
                print("Decisão aplicada:", decision.__str__())
                action = self.decisions[decision]
                break
        print("Ações que devem ser executadas:", action)
        return action
        
    def add_match_route_actions_in_host(self, request, host):
        """
        Adiciona um match, uma rota e ações ao host. Isso é feito após a decisão do controlador e utilizando o método add_match_actions do host.

        Args:
            request (list): Lista com as informações da request.
            host (Host): Host que terá o match, a rota e as ações adicionadas.
        """
        # Obtém as ações que devem ser executadas de acordo com as decisões do controlador.
        actions = self.apply_decision(request)
        # Calcula a rota para o destino (segundo item da lista) da request.
        route = self.calculate_route(request[1])
        # Adiciona a rota e as ações ao host.
        host.add_match_actions(request=request, route=route, actions=actions)
    
    #TODO: Implementar método que adiciona as informações necessárias para as ações. Por exemplo os hosts entre a criação do EPR e o tempo do time_slot.