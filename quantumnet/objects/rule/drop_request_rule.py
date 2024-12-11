from .rule import Rule
from ..action import DropRequestAction

class DropRequestRule(Rule):
    def __init__(self, request, route, controller):
        super().__init__("BasicRoule")
        self.controller = controller
        actions = {}
        
    def behavior(self):
        pass
    
    def prepare(self, controller):
        pass