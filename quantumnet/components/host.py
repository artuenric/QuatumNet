
from ..objects import Logger, Qubit

class Host():
    def __init__(self, host_id: int, probability_on_demand_qubit_create: float = 0.5, probability_replay_qubit_create: float = 0.5, max_qubits_create: int = 10, memory_size: int = 10) -> None:
        # Sobre a rede
        self._host_id = host_id
        self._connections = []
        # Sobre o host
        self._memory = []
        self._memory_size = memory_size
        self._max_qubits_create = max_qubits_create
        self._probability_on_demand_qubit_create = probability_on_demand_qubit_create
        self._probability_replay_qubit_create = probability_replay_qubit_create
        self._flow_table = self.start_flow_table()
        # Sobre a execução
        self.logger = Logger.get_instance()
    
    def __str__(self):
        return f'{self.host_id}'
    
    @property
    def host_id(self):
        """
        ID do host. Sempre um inteiro.

        Returns:
            int : Nome do host.
        """
        return self._host_id
    
    @property
    def connections(self):
        """
        Conexões do host.

        Returns:
            list : Lista de conexões.
        """
        return self._connections
    
    @property
    def memory(self):
        """
        Memória do host.

        Returns:
            list : Lista de qubits.
        """
        return self._memory
    
    @property
    def flow_table(self):
        """
        Tabela de roteamento do host.
        Returns:
            dict : Tabela de roteamento.
        """
        return self._flow_table
    
    def get_last_qubit(self):
        """
        Retorna o último qubit da memória.

        Returns:
            Qubit : Último qubit da memória.
        """
        try:
            q = self.memory[-1]
            self.memory.remove(q)
            return q
        except IndexError:
            raise Exception('Não há mais qubits na memória.')
    
    def add_connection(self, host_id_for_connection: int):
        """
        Adiciona uma conexão ao host. Uma conexão é um host_id, um número inteiro.

        Args:
            host_id_for_connection (int): Host ID do host que será conectado.
        """
        
        if type(host_id_for_connection) != int:
            raise Exception('O valor fornecido para host_id_for_connection deve ser um inteiro.')
        
        if host_id_for_connection not in self.connections:
            self.connections.append(host_id_for_connection),

    def add_qubit(self, qubit: Qubit):
        """
        Adiciona um qubit à memória do host.

        Args:
            qubit (Qubit): O qubit a ser adicionado.
        """
        
        self.memory.append(qubit)
        Logger.get_instance().debug(f'Qubit {qubit.qubit_id} adicionado à memória do Host {self.host_id}.')

    def info(self):
        """
        Retorna informações sobre o host.
        Returns:
            dict : Informações sobre o host.
        """

        return {
            'host_id': self.host_id,
            'memory': len(self.memory),
            'routing_table': "No registration" if self.routing_table == None else self.routing_table
        }
    
    def start_flow_table(self):
        """
        Inicia a tabela de fluxo do host.
        """
        #[match]: (roule)
        # o mesmo que
        #[match]: ([roule], [route])
        
        return {
        }
    
    def requests_match_roule(self, request):
        """
        Requisita uma ação de um match na tabela de fluxo ao controlador.
        
        Returns:
            list : Retorna a ação que deve ser executada.
        """
        #TODO: Implementar a busca por match na tabela de fluxo.
        pass
    
    def find_roule_by_request(self, request):
        """
        Verifica se há ações para um match na tabela de fluxo, dado uma request.
        
        Args:
            request (list): Lista com as informações da request.
        
        Returns:
            list : Caso haja match, retorna a regra (lista de ações que devem ser executadas). Caso contrário, retorna False.
            
        """
        # Percorre a tabela de fluxo.
        for match in self._flow_table:
            # Se o segundo item da request (o destino) for igual ao primeiro item do match (o destino).
            if request[1] == match[0]:
                # Se o terceiro item da request (a Fmin) for menor ou igual ao segundo item do match (a Fmin).
                if request[2] <= match[1]:
                    # Se o quarto item da request (o número de pares EPR) for maior ou igual ao terceiro item do match (o número de pares EPR).
                    if request[3] <= match[2]:
                        return self._flow_table[match]
        return False
    
    def add_match_route_roule(self, request, route, roule):
        """
        Adiciona um match, rota e ação à tabela de fluxo.
        """
        self._flow_table[(request[1], request[2], request[3])] = (route, roule)
        
        
    
## Match fica na tabela de fluxo, são as chaves do dicionário.
## Request é o que chega, comparado ao match, são diferentes apenas pelo primeiro item. Que no request é o host_id do host que está enviando a requisição.
## Route é a rota que o pacote deve seguir.
# Actions são as ações que devem ser executadas. Especificamente classes. O controlador executará essas ações por meio da rede.
# Roules são conjuntos de ações.