from .action import Action
class PurificationAction(Action):
    def __init__(self, alice, bob, controller):
        """
        Purifica um par de Bell entre dois nós.
        
        Args:
            alice (int): Id do nó Alice.
            bob (int): Id do nó Bob.
            controller (Controller): Controlador da simulação.
        """
        super().__init__(action_name = "PURIFICATION", action_description = "Purify a Bell pair between two hosts.")
        self.set_alice(alice)
        self.set_bob(bob)
        self.controller = controller
        
    def __repr__(self):
        return f"Purification({self.nodes[0]}-{self.nodes[1]})"
    
    def run(self):
        pass