from .time import time
import random
import math

class Qubit():
    def __init__(self, qubit_id: int, initial_fidelity: float = 1) -> None:
        self.qubit_id = qubit_id
        self._relaxed = False
        self._qubit_state = 0
        self._creation_time = time.get_current_time()
        self._life_time = 0
        # Sobre a fidelidade
        self._initial_fidelity = initial_fidelity
        self._current_fidelity = self._initial_fidelity
        self.t2_time = 100  # Tempo de decoerência T2

    def __str__(self):
        return f"Qubit {self.qubit_id} with state {self._qubit_state}"

    def update_fidelity(self):
        self._current_fidelity = random.uniform(0, 1)

    def get_initial_fidelity(self):
        return self._initial_fidelity

    def get_current_fidelity(self):
        timeslot = time.get_current_time()
        if self._initial_fidelity < 0 or self._initial_fidelity > 1:
            raise ValueError("Initial fidelity must be between 0 and 1.")
        if timeslot < 0:
            raise ValueError("Time-slot must be non-negative.")
        # Fidelity decay formula
        fidelity = self._initial_fidelity * math.exp(-self._life_time / self.t2_time)
        return fidelity    

    def set_current_fidelity(self, new_fidelity: float):
            """Define a fidelidade atual do qubit."""
            self._current_fidelity = new_fidelity

    def measure(self):
        """Realiza a medição do qubit no estado atual."""
        return self._qubit_state

    def relax(self):
        """Relaxa o qubit, zerando a fidelidade."""
        self._current_fidelity = 0
        self._relaxed = True
        
    def update_time(self, current_time):
        """Atualiza a fidelidade do qubit de acordo com o tempo."""
        # Atualiza o tempo de vida do qubit
        self._life_time += 1
        # Se a fidelidade atual for menor que 0.2, relaxa o qubit
        if self.get_current_fidelity() < 0.2:
            self.relax()
        # self._current_fidelity = self.get_current_fidelity()