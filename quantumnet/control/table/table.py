from abc import ABC, abstractmethod

class Table(ABC):
    def __init__(self):
        self.conditions = self.set_conditions()

    @abstractmethod
    def set_conditions(self):
        """
        Define as condições do controlador para escolher as regras.
        """
        pass
        
    def add_conditions(self, conditions, rule):
        """
        Adiciona uma condição e uma regra a tabela.
        """
        self.conditions_table[conditions] = rule
    
    def draw(self):
        """
        Desenha a tabela de condições e regras.
        """
        for conditions, rule in self.conditions_table.items():
            print(f"Condições: {conditions} -> Regra: {rule}")