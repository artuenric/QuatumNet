import networkx as nx
from ..components import Network, Host
from ..control.condition import SourceIsTargetCondition, HighFidelityCondition, NormalE2ECondition
from ..control.rule import DropRequestRule, BasicRuleProactive
from ..control.table import ReactiveTable
class Controller():
    def __init__(self, network):
        self.network = network
        self.hosts = None
        self.links = None
        self.conditions_table = None
        self.set_conditions_table(ReactiveTable())
        self.default_ttl = 10
    
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
    
    def set_conditions_table(self, table):
        """
        Define as condições do controlador para escolher as regras.

        Returns:
            dict: Dicionário com as condições e as regras correspondentes.
        """
        self.conditions_table = table.conditions
        
    def apply_conditions(self, request):
        """
        Aplica uma condição do controlador para um match específico. Retorna a ação que deve ser executada.

        Args:
            request (Request): Requisição que contém as informações da comunicação.
        
        Returns:
            rule (rule): Regra com as ações que devem ser executadas.
        """
        
        for condition in self.conditions_table:
            # Retorna a ação correspondente as decisões da tabela que são válidas para a request.
            if all(d.verify(request) for d in condition):
                print("Decisão aplicada:", condition)
                return self.conditions_table[condition]

        return [DropRequestRule]
        
    def add_match_route_rule_in_host_reactive(self, request):
        """
        Adiciona um match, uma rota e ações ao host. Isso é feito após a decisão do controlador e utilizando o método add_match_actions do host.
        Nesse cenário, o controlador é reativo, ou seja, ele toma decisões com base na chegada de uma request.

        Args:
            request (Request): Requisição que contém as informações da comunicação.
        """
        alice, bob, fmin, neprs = request.alice, request.bob, request.fmin, request.neprs
        frange = (fmin-0.1,fmin+0.1)
        # Obtém as ações que devem ser executadas de acordo com as decisões do controlador.
        rule = self.apply_conditions(request)
        # Calcula a rota para o destino (segundo item da lista) da request.
        route = self.calculate_route(request.alice, request.bob)
        # Qualifica as ações de acordo com as informações da request.
        rule = self.qualify_rule(rule, route)
        # Adiciona a rota e as ações ao host.
        self.network.get_host(alice).add_match_route_rule(bob, frange, neprs, route, rule)

    def add_match_route_rule_in_host_proactive(self, alice, bob, frange, neprs):
        """
        Adiciona um match, uma rota e ações ao host. Isso é feito após a decisão do controlador e utilizando o método add_match_actions do host.
        Nesse cenário, o controlador é proativo, ou seja, ele preenche a tabela com base em informações da rede.

        Args:
            alice (int): ID do host de origem.
            bob (int): ID do host de destino.
            frange (tuple): Range de fidelidade para a comunicação.
            neprs (int): Número de EPRs necessários para a comunicação.
        """
        route = self.calculate_route(alice, bob)
        # Cria a regra
        rule = BasicRuleProactive
        # Qualifica as ações de acordo com as informações da request.
        rule = self.qualify_rule(rule, route)
        # Adiciona a rota e as ações ao host.
        self.network.get_host(alice).add_match_route_rule(bob, frange, neprs, route, rule)

    def qualify_rule(self, rule, route):
        """
        Qualifica uma regra de acordo com as informações da request e da rede.

        Args:
            request (list): Lista com as informações da request.
            rule (rule): Regra com as ações que devem ser executadas.
            route (list): Lista com a rota para o destino.
        """
        return rule(route, self)
    
    def run_rule(self, rule):
        """
        Executa as ações de um rule.

        Args:
            rule (dict): Dicionário com as ações que devem ser executadas.
        """
        rule.run()
    
    def avg_route_fidelity(self, route, timeslot):
        """
        Calcula a fidelidade média de uma rota.

        Args:
            route (list): Lista com a rota para o destino.
            timeslot (int): Timeslot atual.
            
        Returns:
            float : Fidelidade média da rota.
        """
       
        total_fidelity = 0
        for a, b in zip(route[:-1], route[1:]):
            epr = self.network.get_eprs_from_edge(a, b)[0]
            fidelities = epr.get_current_fidelities(timeslot)
            avg_fidelity = sum(fidelities) / len(fidelities) if fidelities else 0
            total_fidelity += avg_fidelity
        
        return total_fidelity / (len(route) - 1) if len(route) > 1 else 0