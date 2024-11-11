from .action import Action
class SwapAction(Action):
    def __init__(self, nodes, controller):
        super().__init__(action_name = "SWAP", action_description = "Swap two qubits between two hosts.", controller = controller)
        self.set_nodes(nodes)
        
    def __repr__(self):
        return f"Swap({self.nodes[0]}-{self.nodes[1]})"
    
    def run(self):
        self.controller.network.networklayer.entanglement_swapping(self.nodes[0], self.nodes[1])