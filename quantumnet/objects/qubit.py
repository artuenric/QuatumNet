from .time import time
import random
import math

class Qubit():
    def __init__(self, host, initial_fidelity: float = 1) -> None:
        # Sobre as informações do qubit
        self.host = host
        self.qubit_id = self.set_id()
        self._creation_time = time.get_current_time()
        self._life_time = 0
        # Sobre o estado do qubit
        self._relaxed = False
        self._qubit_state = 0
        # Sobre a fidelidade
        self._initial_fidelity = initial_fidelity
        self._current_fidelity = self._initial_fidelity
        self.t2_time = 10  # Tempo de decoerência T2
        
    def __repr__(self):
        return self.qubit_id

    def set_id(self):
        return f"Q{hex(id(self))[-4:].upper()}.{self.host.count_qubit}"
    
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
        # A fidelidade do qubit é zerada
        self._current_fidelity = 0
        # O qubit é relaxado
        self._relaxed = True
        # O qubit é removido da memória do host
        self.host.remove_qubit(self)
        # O qubit é removido do gerenciador de tempo
        time.qubits.remove(self)
        
    def update_time(self):
        """Atualiza a fidelidade do qubit de acordo com o tempo."""
        # Atualiza o tempo de vida do qubit
        self._life_time += 1
        # Se a fidelidade atual for menor que 0.2, relaxa o qubit
        if self.get_current_fidelity() < 0.4:
            self.relax()
        # self._current_fidelity = self.get_current_fidelity()