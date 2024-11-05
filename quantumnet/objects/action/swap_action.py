from .action import Action
class SwapAction(Action):
    def __init__(self, pair_1, pair_2):
        super().__init__(action_name = "SWAP", action_description = "Swap two qubits between two hosts.")
        self.pairs = (pair_1, pair_2)
        