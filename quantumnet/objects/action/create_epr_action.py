from .action import Action
class CreateEPRAction(Action):
    def __init__(self, alice, bob, controller):
        """
        Cria um par EPR entre dois nós.

        Args:
            alice (int): Id do nó Alice.
            bob (int): Id do nó Bob.
            controller (Controller): Controlador da simulação.
        """
        super().__init__(action_name = "CREATE EPR", action_description = "Create an EPR pair between two hosts.", controller = controller)
        self.set_alice(alice)
        self.set_bob(bob)
    
    def __repr__(self):
        return f"CreateEPR({self.alice}-{self.bob})"
    
    def run(self):
        """
        Cria um par EPR entre dois nós.
        """
        self.controller.network.physical.echp_on_demand(self.alice, self.bob)