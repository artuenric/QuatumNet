from .action import Action
class PurificationAction(Action):
    def __init__(self):
        super().__init__(action_name = "PURIFICATION", action_description = "Purify a Bell pair between two hosts.")