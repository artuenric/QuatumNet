import networkx as nx
from ..components import Network, Host
from ..objects.decision import Decision_X

class Controller():
    def __init__(self, network):
        self.network = network
        self.hosts = None
        self.links = None
        self.decisions = self.set_decisions()
        
    def set_decisions(self):
        """
        Define as decisões do controlador para escolher as ações.
        """
        decision = {
            (Decision_X(),): [0]
        }
        return decision
    
    def add_match_action(self, match, action, host):
        """
        Adiciona uma regra de match-action para um host específico.

        Args:
            host (Host): Host que terá a regra adicionada.
            match (lista): Lista de itens que devem ser correspondidos.
            action (ainda não sei):
        """
        pass
    
    def apply_decision(self, request):
        """
        Aplica uma decisão do controlador para um match específico. Retorna a ação que deve ser executada.

        Args:
            info (lista): Lista com as informações da request.
        
        Returns:
            action (lista): Lista com as ações que devem ser executadas.
        """
        
        action = -1
        for decision in self.decisions:
            # Retorna a ação correspondente as decisões da tabela que são válidas para a request.
            if all(d.verify(request) for d in decision):   
                action = self.decisions[decision]
                break
        return action
    
    def set_actions(self, request, host):
        action = self.apply_decision(request)
        
        pass
    