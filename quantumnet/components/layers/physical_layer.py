from ...objects import logger, Qubit, Epr, time
from ...components import Host
from random import uniform

class PhysicalLayer:
    def __init__(self, network):
        """
        Inicializa a camada física.
        
        """
        self.max_fidelity = 1
        self.min_fidelity = 0.5
        self._network = network
        self._initial_qubits_fidelity = uniform(self.max_fidelity, self.min_fidelity)    
        
    def __str__(self):
        """ Retorna a representação em string da camada física. 
        
        Returns:
            str: Representação em string da camada física.
        """
        return f'Physical Layer {self.physical_layer_id}'
    
    def create_qubit(self, host_id: int):
        """Cria um qubit e adiciona à memória do host especificado.

        Args:
            host_id (int): ID do host onde o qubit será criado.

        Raises:
            Exception: Se o host especificado não existir na rede.
        """
        logger.debug(f'Criando qubit no host {host_id}.')
        
        if host_id not in self._network.hosts:
            raise Exception(f'Host {host_id} não existe na rede.')
        
        # Obtém o host da rede
        host = self._network.get_host(host_id)
        
        # Incrementa o número de qubits criados na rede
        self._network.registry_of_resources['qubits created'] += 1
        
        # Cria o qubit
        qubit = Qubit(host)
        host.add_qubit(qubit)
        
        logger.debug(f'Qubit {qubit} criado no host {host_id}.')
        
        # Inscreve o qubit no time_slot
        time.subscribe_qubit(qubit)

    def create_epr_pair(self, channel, fidelity: float = 1.0):
        """Cria um par de qubits entrelaçados.

        Returns:
            Qubit, Qubit: Par de qubits entrelaçados.
        """
        logger.debug(f'Criando par EPR no canal {channel} com fidelidade {fidelity}.')
        
        # Incrementa o número de EPRs criados na rede
        self._network.registry_of_resources['eprs created'] += 1
        
        # Cria o par EPR
        epr = Epr(self._network, channel, fidelity)
        
        return epr

    def add_epr_to_channel(self, epr: Epr, channel: tuple):
        """Adiciona um par EPR ao canal.

        Args:
            epr (Epr): Par EPR.
            channel (tuple): Canal.
        """
        u, v = channel
        if not self._network.graph.has_edge(u, v):
            self._network.graph.add_edge(u, v, eprs=[])
        self._network.graph.edges[u, v]['eprs'].append(epr)
        logger.debug(f'Par EPR {epr} adicionado ao canal {channel}.')
        
        # Inscreve o par EPR no time_slot
        logger.debug(f'Inscrição do par EPR {epr} no time.')
        time.subscribe_epr(epr)

    def remove_epr_from_channel(self, epr: Epr, channel: tuple):
        """
        Remove um par EPR do canal.

        Args:
            epr (Epr): Par EPR a ser removido.
            channel (tuple): Canal.
        """
        u, v = channel
        if not self._network.graph.has_edge(u, v):
            logger.warn(f'Canal {channel} não existe.')
        try:
            self._network.graph.edges[u, v]['eprs'].remove(epr)
            time.eprs.remove(epr)
            logger.debug(f'Par EPR {epr} removido do canal {channel}.')
        except ValueError:
            logger.debug(f'Par EPR {epr} não encontrado no canal {channel}.')
    
    def entanglement_creation_heralding_protocol(self, alice_id: int, bob_id: int):
        """
        Protocolo de criação de emaranhamento com sinalização.
        
        Args:
            alice_id (int): ID do host Alice.
            bob_id (int): ID do host Bob.
        
        Returns:
            bool: True se o protocolo foi bem sucedido, False caso contrário.
        """
        logger.debug(f'Protocolo ECHP entre {alice_id} e {bob_id}.')
        
        # Obtém os hosts da rede
        alice, bob = self._network.get_host(alice_id), self._network.get_host(bob_id)
        
        qubit1 = alice.get_last_qubit()
        qubit2 = bob.get_last_qubit()

        if (qubit1 == False) or (qubit2 == False):
            logger.info(f'Não há qubits suficientes para o protocolo ECHP entre {alice_id} e {bob_id}.')
        else:
            # Fidelidade leva em consideração a decoerência
            q1 = qubit1.get_current_fidelity()
            q2 = qubit2.get_current_fidelity()

            epr_fidelity = q1 * q2
            logger.debug(f'Par epr criado com fidelidade {epr_fidelity}')
            epr = self.create_epr_pair((alice_id, bob_id), epr_fidelity)

            # Adiciona o EPR ao canal da rede
            self.add_epr_to_channel(epr, (alice_id, bob_id))
            
            # Registra os qubits usados na rede
            self._network.registry_of_resources['qubits used'] += 2