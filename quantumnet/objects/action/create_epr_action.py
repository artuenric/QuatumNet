from .action import Action
class CreateEPRAction(Action):
    def __init__(self, nodes, controller):
        super().__init__(action_name = "CREATE_EPR", action_description = "Create an EPR pair between two hosts.", controller = controller)
        self.set_nodes(nodes)
    
    def run(self):
        self.controller.network.physical.create_epr_pair(self.nodes[0], self.nodes[1])