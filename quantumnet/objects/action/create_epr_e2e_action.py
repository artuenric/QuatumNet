from .action import Action
class CreateEPRE2EAction(Action):
    def __init__(self):
        super().__init__(action_name = "CREATE EPR E2E", action_description = "Create EPR pairs end to end.")