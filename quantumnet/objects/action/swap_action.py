from .action import Action
class SwapAction(Action):
    def __init__(self, alice, bob, middle, controller):
        super().__init__(action_name = "SWAP", action_description = "Swap two qubits between two hosts.", controller = controller)
        self.alice = alice
        self.bob = bob
        self.midlle_node = middle
        
    def __repr__(self):
        return f"Swap({self.alice}-{self.midlle_node}-{self.bob})"
    
    def run(self):
        self.controller.network.networklayer.swap(self.alice, self.bob, self.midlle_node)