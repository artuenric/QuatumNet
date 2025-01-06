
from quantumnet.components import Network, Controller
from .generate_requests import generate_traffic
from abc import ABC, abstractmethod
from quantumnet.objects import time

class Sim(ABC):
    def __init__(self, network_info, controller_info, request_info):
        # Rede
        self.network = Network()
        self.network.n_initial_qubits = network_info['n_initial_qubits']
        self.network.n_initial_eprs = network_info['n_initial_eprs']
        self.network.set_ready_topology(network_info['topology_name'], network_info['topology_params'])
        self.time_to_refill = network_info['time_to_refill']
        # Controlador
        self.controller = Controller(self.network)
        self.controller.default_ttl = controller_info['default_ttl']
        # Requisições
        self.requests = generate_traffic(request_info)
    
    def update_time(self, n_time_slots):
        """
        Atualiza o tempo e as regras

        Args:
            time_for_update (int): Tempo para incrementar o time-slot.
        """
        # Atualiza o tempo
        for t in range(n_time_slots):
            time.increment()
            # Atualiza os recursos de 10 em 10
            if time.get_current_time() % self.time_to_refill== 0:
                self.network.refresh_resources(num_qubits=self.network.n_initial_qubits, num_eprs=self.network.n_initial_eprs)
                print(f"[Time {time.get_current_time()}] Recursos atualizados")