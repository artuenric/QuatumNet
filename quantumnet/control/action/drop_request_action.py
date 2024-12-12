from .action import Action
class DropRequestAction(Action):
    def __init__(self):
        super().__init__(action_name = "DROP", action_description = "Ignore request.")
    
    def __repr__(self):
        return "Drop request"
    
    def run(self):
        pass