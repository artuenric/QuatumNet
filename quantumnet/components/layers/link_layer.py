import networkx as nx
from quantumnet.components import Host
from quantumnet.objects import logger

class LinkLayer:
    def __init__(self, network):
        """
        Inicializa a camada de enlace.
        
        Args:
            network : Network : Rede.
            physical_layer : PhysicalLayer : Camada física.
        """
        self._network = network

    def __str__(self):
        """ Retorna a representação em string da camada de enlace. 
        
        Returns:
            str : Representação em string da camada de enlace.
        """
        return 'Link Layer'
