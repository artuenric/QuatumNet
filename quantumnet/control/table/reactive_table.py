from .table import Table
from ..condition import SourceIsTargetCondition, HighFidelityCondition, NormalE2ECondition
from ..rule import DropRequestRule, HighFidelityRule, BasicRuleReactive

class ReactiveTable(Table):
    def __init__(self):
        super().__init__()
        
    def set_conditions(self):
        """
        Define as condições do controlador para escolher as regras.
        """
        return {
            (SourceIsTargetCondition(),): DropRequestRule,        
            (HighFidelityCondition(),): HighFidelityRule,
            (NormalE2ECondition(),): BasicRuleReactive,
        }