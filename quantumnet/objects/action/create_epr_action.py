from .action import Action
class CreateEPRAction(Action):
    def __init__(self, nodes, controller):
        super().__init__(action_name = "CREATE EPR", action_description = "Create an EPR pair between two hosts.", controller = controller)
        self.set_nodes(nodes)
    
    def __repr__(self):
        return f"CreateEPR({self.nodes[0]}-{self.nodes[1]})"
    
    def run(self):
        """
        Cria um par EPR entre dois nós.
        """
        self.controller.network.physical.create_epr_pair(self.nodes[0], self.nodes[1])