from .roule import Roule
from ..action import DropRequestAction

class DropRequestRoule(Roule):
    def __init__(self, controller):
        super().__init__("BasicRoule")
        self.controller = controller
        actions = {}
        
    def behavior(self):
        pass
    
    def prepare(self, controller):
        pass