import random
from math import exp
from .time import time
class Epr():
    def __init__(self,  epr_id: int, initial_fidelity: float = None) -> None:
        self._epr_id = epr_id
        self._relaxed = False
        self._creation_time = time.get_current_time()
        self._life_time = 0
        self._initial_fidelity = initial_fidelity  if initial_fidelity is not None else random.uniform(0, 1)
        self._current_fidelity = initial_fidelity  if initial_fidelity is not None else random.uniform(0, 1)
        self.t2_time = 100  # Tempo de decoerência T2
    
    @property
    def epr_id(self):
        return self._epr_id
    
    def get_initial_fidelity(self):
        return self._initial_fidelity
    
    def get_current_fidelity(self):
        timeslot = time.get_current_time()
        if self._initial_fidelity < 0 or self._initial_fidelity > 1:
            raise ValueError("Initial fidelity must be between 0 and 1.")
        if timeslot < 0:
            raise ValueError("Time-slot must be non-negative.")
        # Fidelity decay formula
        fidelity = self._initial_fidelity * exp(-self._life_time / self.t2_time)
        return fidelity
    
    def set_fidelity(self, new_fidelity: float):
        """Define a nova fidelidade do par EPR."""
        self._current_fidelity = new_fidelity
    
    def relax(self):
        """Relaxa o par EPR, zerando a fidelidade."""
        self._current_fidelity = 0
        self._relaxed = True
    
    def update_time(self, current_time):
        """Atualiza a fidelidade do par EPR de acordo com o tempo."""
        # Atualiza o tempo de vida do par EPR
        self._life_time += 1
        # Se a fidelidade atual for menor que 0.2, relaxa o par EPR
        if self.get_current_fidelity() < 0.5:
            self.relax()