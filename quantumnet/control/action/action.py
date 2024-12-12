from abc import ABC, abstractmethod
class Action(ABC):
    def __init__(self, action_name: str, action_description: str, controller):        
        self.action_name = action_name
        self.action_description = action_description
        self.nodes = () # origem e destino
        self.controller = controller
        self.time_slot = None
    
    def set_alice(self, id_alice):
        """
        Define o nó Alice da ação por meio de seu ID.

        Args:
            id_alice (int): ID do nó Alice.
        """
        self.alice = id_alice
    
    def set_bob(self, bob):
        """
        Define o nó Bob da ação por meio de seu ID.
        
        Args:
            bob (int): ID do nó Bob.
        """
        self.bob = bob
        
    @abstractmethod
    def run(self):
        """
        Executa a ação.
        """
        pass