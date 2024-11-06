from .action import Action
class PurificationAction(Action):
    def __init__(self, nodes):
        super().__init__(action_name = "PURIFICATION", action_description = "Purify a Bell pair between two hosts.")
        self.nodes = nodes
        
    def __repr__(self):
        return f"Purification({self.nodes[0]}-{self.nodes[1]})"
    
    def run(self):
        pass