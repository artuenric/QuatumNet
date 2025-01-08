import random
from quantumnet.components import Host
from quantumnet.objects import Qubit, logger

class ApplicationLayer:
    def __init__(self, network):
        """
        Inicializa a camada de aplicação do protocolo QKD (Distribuição Quântica de Chaves).

        Args:
            network: objeto que representa a rede quântica.
            transport_layer: camada de transporte da rede.
            network_layer: camada de rede da rede.
            link_layer: camada de enlace da rede.
            physical_layer: camada física da rede.
        """
        self._network = network

    def __str__(self):
        """ Retorna a representação em string da camada de aplicação. 
        
        Returns:
            str: Representação em string da camada de aplicação.
        """
        return f'Application Layer'