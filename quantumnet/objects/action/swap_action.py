from .action import Action
class SwapAction(Action):
    def __init__(self):
        super().__init__(action_name = "SWAP", action_description = "Swap two qubits between two hosts.")
        