from .action import Action
class HighPurificationAction(Action):
    def __init__(self):
        super().__init__(action_name = "HIGH PURIFICATION", action_description = "Purify all pairs between end-to-end connection of alice and bob.")