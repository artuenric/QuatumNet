import networkx as nx
from ..components import Network, Host
from ..objects.condition import SourceIsTargetCondition, HighFidelityCondition, NormalE2ECondition
#from ..objects.action import DropRequestAction, HighPurificationAction, CreateEPRAction, SwapAction, PurificationAction
from ..objects.rule import BasicRule, HighFidelityRule, DropRequestRule

class Controller():
    def __init__(self, network):
        self.network = network
        self.hosts = None
        self.links = None
        self.conditions = self.set_conditions()
    
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
            
    def set_conditions(self):
        """
        Define as condições do controlador para escolher as regras.
        """
        return {
            (SourceIsTargetCondition(),): DropRequestRule,            
            (HighFidelityCondition(),): HighFidelityRule,
            (NormalE2ECondition(),): BasicRule,
        }
    
    def apply_conditions(self, request):
        """
        Aplica uma condição do controlador para um match específico. Retorna a ação que deve ser executada.

        Args:
            request (lista): Lista com as informações da request.
        
        Returns:
            rule (rule): Regra com as ações que devem ser executadas.
        """
        
        for condition in self.conditions:
            # Retorna a ação correspondente as decisões da tabela que são válidas para a request.
            if all(d.verify(request) for d in condition):
                print("Decisão aplicada:", condition)
                return self.conditions[condition]

        return [DropRequestRule]
        
    def add_match_route_rule_in_host(self, request, host):
        """
        Adiciona um match, uma rota e ações ao host. Isso é feito após a decisão do controlador e utilizando o método add_match_actions do host.

        Args:
            request (list): Lista com as informações da request.
            host (Host): Host que terá o match, a rota e as ações adicionadas.
        """
        # Obtém as ações que devem ser executadas de acordo com as decisões do controlador.
        rule = self.apply_conditions(request)
        # Calcula a rota para o destino (segundo item da lista) da request.
        route = self.calculate_route(request[0], request[1])
        # Qualifica as ações de acordo com as informações da request.
        rule = self.qualify_rule(request, rule, route)
        # Adiciona a rota e as ações ao host.
        host.add_match_route_rule(request=request, route=route, rule=rule)

    def qualify_rule(self, request, rule, route):
        """
        Qualifica uma regra de acordo com as informações da request e da rede.

        Args:
            request (list): Lista com as informações da request.
            rule (rule): Regra com as ações que devem ser executadas.
            route (list): Lista com a rota para o destino.
        """
        return rule(request, route, self)
    
    def run_rule(self, rule):
        """
        Executa as ações de um rule.

        Args:
            rule (dict): Dicionário com as ações que devem ser executadas.
        """
        rule.run()
    