from .action import Action
class SwapAction(Action):
    def __init__(self, pair_1, pair_2, controller):
        super().__init__(action_name = "SWAP", action_description = "Swap two qubits between two hosts.", controller = controller)
        self.pairs = (pair_1, pair_2)
    
    def __repr__(self):
        return f"Swap({self.pairs[0]}-{self.pairs[1]})"
    
    def run(self):
        pass