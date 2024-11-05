from abc import ABC, abstractmethod
class Action(ABC):
    def __init__(self, action_name: str, action_description: str, controller):        
        self.action_name = action_name
        self.action_description = action_description
        self.nodes = () # origem e destino
        self.controller = controller
        self.time_slot = None
    
    def set_nodes(self, nodes):
        if len(nodes) != 2:
            raise ValueError('Action must have exactly 2 nodes.')
        self.nodes = nodes
        
    @abstractmethod
    def run(self):
        """
        Executa a ação.
        """
        pass