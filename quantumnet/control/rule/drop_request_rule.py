from .rule import Rule
from ..action import DropRequestAction

class DropRequestRule(Rule):
    def __init__(self, route, controller):
        super().__init__("BasicRoule", controller.default_ttl)
        self.controller = controller
        actions = {}
        
    def behavior(self):
        pass
    
    def prepare(self, controller):
        pass