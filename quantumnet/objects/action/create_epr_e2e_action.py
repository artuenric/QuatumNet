from .action import Action
class CreateEPRActionE2E(Action):
    def __init__(self):
        super().__init__(action_name = "CREATE EPR E2E", action_description = "Create EPR pairs end to end.")