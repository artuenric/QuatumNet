from .action import Action
class CreateEPRAction(Action):
    def __init__(self):
        super().__init__(action_name = "CREATE_EPR", action_description = "Create an EPR pair between two hosts.")