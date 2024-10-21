import networkx as nx
from ..components import Network, Host
from ..objects.roules import X_Roule

class Controller():
    def __init__(self, network):
        self.network = network
        self.hosts = None
        self.links = None
        self.roules = [X_Roule()]
        
    def add_match_action(self, match, action, host):
        """
        Adiciona uma regra de match-action para um host específico.

        Args:
            host (Host): Host que terá a regra adicionada.
            match (lista): Lista de itens que devem ser correspondidos.
            action (ainda não sei):
        """
        pass
    
    def apply_roule(self, info):
        """
        Aplica a regra do controlador para um match específico. Retorna a ação que deve ser executada.

        Args:
            info (lista): Lista com as informações da request.
        
        Returns:
            action (ainda não sei): Ação que deve ser executada.
        """
        action = -1
        for roule in self.roules:
            action = roule.verify(info)
            if roule is not -1:
                break
        return action
    
    def set_actions(self, match):
        pass
    