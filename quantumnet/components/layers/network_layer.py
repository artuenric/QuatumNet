import networkx as nx
from quantumnet.components import Host
from quantumnet.objects import Logger, Epr
from random import uniform

class NetworkLayer:
    def __init__(self, network):
        """
        Inicializa a camada de rede.
        
        args:
            network : Network : Rede.
        """
        self._network = network
        self.logger = Logger.get_instance()
        self.avg_size_routes = 0  # Inicializa o tamanho médio das rotas
        self.used_eprs = 0  # Inicializa o contador de EPRs utilizados
        self.used_qubits = 0  # Inicializa o contador de Qubits utilizados
        self.routes_used = {}  # Inicializa o dicionário de rotas usadas 
    def __str__(self):
        """ Retorna a representação em string da camada de rede. 
        
        returns:
            str : Representação em string da camada de rede."""
        return 'Network Layer'

    def get_used_eprs(self):
        """Retorna a contagem de EPRs utilizados na camada de rede."""
        self.logger.debug(f"Eprs usados na camada {self.__class__.__name__}: {self.used_eprs}")
        return self.used_eprs
    
    def get_used_qubits(self):
        self.logger.debug(f"Qubits usados na camada {self.__class__.__name__}: {self.used_qubits}")
        return self.used_qubits

    def swap(self, alice, bob, mid):
        """
        Realiza o swapping de entrelaçamento entre três nós.

        args:
            alice (int): ID do host de origem.
            bob (int): ID do host de destino.
            mid (int): ID do host intermediário.
            
        returns:
            bool: True se o swapping foi bem-sucedido, False caso contrário.
        """
        eprs_alice_mid = self._network.get_eprs_from_edge(alice, mid)
        eprs_mid_bob = self._network.get_eprs_from_edge(mid, bob)   
        
        # Checa se existe pares EPR entre os hosts
        if (len(eprs_alice_mid) <= 0) or (len(eprs_mid_bob) <= 0):
            return False
        
        # Coleta os pares EPR
        epr1 = eprs_alice_mid[0]
        epr2 = eprs_mid_bob[0]
                    
        # Remove os pares EPR dos canais
        self._network.physicallayer.remove_epr_from_channel(epr1, (alice, mid))
        self._network.physicallayer.remove_epr_from_channel(epr2, (mid, bob))
        
        # Mede a fidelidade dos pares EPR
        fidelity1 = epr1.get_current_fidelity()
        fidelity2 = epr2.get_current_fidelity()
        
        # Calcula a probabilidade de sucesso do entanglement swapping
        success_prob = fidelity1 * fidelity2 + (1 - fidelity1) * (1 - fidelity2)
        
        # Calcula a nova fidelidade do par EPR virtual
        new_fidelity = (fidelity1 * fidelity2) / ((fidelity1 * fidelity2) + (1 - fidelity1) * (1 - fidelity2))
        virtual_epr = self._network.physicallayer.create_epr_pair((alice, bob), new_fidelity)

        # Se o canal entre node1 e node3 não existir, adiciona um novo canal
        if not self._network.graph.has_edge(alice, bob):
            self._network.graph.add_edge(alice, bob, eprs=[], virtual_link=True)

        # Adiciona o par EPR virtual ao canal entre node1 e node3
        self._network.physicallayer.add_epr_to_channel(virtual_epr, (alice, bob))

        # Atualiza o contador de EPRs utilizados
        self.used_eprs += 1

        return True