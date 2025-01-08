import networkx as nx
from quantumnet.components import Host
from quantumnet.objects import logger, Epr
from random import uniform

class NetworkLayer:
    def __init__(self, network):
        """
        Inicializa a camada de rede.
        
        args:
            network : Network : Rede.
        """
        self._network = network

    def __str__(self):
        """ Retorna a representação em string da camada de rede. 
        
        returns:
            str : Representação em string da camada de rede."""
        return 'Network Layer'

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
        logger.debug(f'Entanglement swapping entre {alice} e {bob} via {mid}.')
        
        # Checa se o entrelaçamento é possível
        eprs_alice_mid = self._network.get_eprs_from_edge(alice, mid)
        eprs_mid_bob = self._network.get_eprs_from_edge(mid, bob)   
        if (eprs_alice_mid == False) or (eprs_mid_bob is False):
            logger.info(f'Entanglement swapping entre {alice} e {bob} não é possível.')
            return False
        
        # Checa se existe pares EPR entre os hosts
        if (len(eprs_alice_mid) <= 0) or (len(eprs_mid_bob) <= 0):
            logger.info(f'Não há EPRs suficientes para o entanglement swapping entre {alice} e {bob}.')
            return False
        
        # Coleta os pares EPR
        epr1 = eprs_alice_mid[0]
        epr2 = eprs_mid_bob[0]
                    
        # Remove os pares EPR dos canais
        self._network.physicallayer.remove_epr_from_channel(epr1, (alice, mid))
        self._network.physicallayer.remove_epr_from_channel(epr2, (mid, bob))
        logger.debug(f'Pares EPR {epr1} e {epr2} removidos dos canais ({alice}, {mid}) e ({mid}, {bob}).')
        
        # Mede a fidelidade dos pares EPR
        fidelity1 = epr1.get_current_fidelity()
        fidelity2 = epr2.get_current_fidelity()
        
        # Calcula a probabilidade de sucesso do entanglement swapping
        success_prob = fidelity1 * fidelity2 + (1 - fidelity1) * (1 - fidelity2)
        
        # Calcula a nova fidelidade do par EPR virtual
        new_fidelity = (fidelity1 * fidelity2) / ((fidelity1 * fidelity2) + (1 - fidelity1) * (1 - fidelity2))
        virtual_epr = self._network.physicallayer.create_epr_pair((alice, bob), new_fidelity)
        logger.debug(f'Par EPR virtual criado com fidelidade {new_fidelity}.')
        
        # Se o canal entre node1 e node3 não existir, adiciona um novo canal
        if not self._network.graph.has_edge(alice, bob):
            logger.info(f'Não existe canal físico entre {alice} e {bob}. Adicionando canal virtual.')
            self._network.graph.add_edge(alice, bob, eprs=[], virtual_link=True)

        # Adiciona o par EPR virtual ao canal entre node1 e node3
        self._network.physicallayer.add_epr_to_channel(virtual_epr, (alice, bob))
        logger.debug(f'Par EPR virtual {virtual_epr} adicionado ao canal virtual ({alice}, {bob}).')
