from tabulate import tabulate
from ..objects import Logger, Qubit, time
from math import exp

class Host():
    def __init__(self, host_id: int, probability_on_demand_qubit_create: float = 0.5, probability_replay_qubit_create: float = 0.5, memory_size: int = 10) -> None:
        # Sobre a rede
        self._host_id = host_id
        self._connections = []
        # Sobre o host
        self._memory = []
        self._count_qubit = 0
        self._memory_size = memory_size
        self._probability_on_demand_qubit_create = probability_on_demand_qubit_create
        self._probability_replay_qubit_create = probability_replay_qubit_create
        self._flow_table = self.start_flow_table()
        self._rule_index = {}
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
    def count_qubit(self):
        """
        Retorna a quantidade de qubits na memória.

        Returns:
            int : Quantidade de qubits.
        """
        return self._count_qubit
    
    @property
    def flow_table(self):
        """
        Tabela de roteamento do host.
        Returns:
            dict : Tabela de roteamento.
        """
        return self._flow_table
    
    def draw_flow_table(self):
        """
        Desenha a tabela de fluxo do host em formato de tabela.
        """
        table = []
        for match, (route, rule) in self._flow_table.items():
            table.append([match, route, rule])

        print(tabulate(table, headers=["Match", "Route", "Rule"], tablefmt="grid"))

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
        
        self._count_qubit += 1
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
        #[match]: (rule)
        # o mesmo que
        #[match]: ([rule], [route])
        
        return {
        }
    
    
    def find_rule_by_request(self, request):
        """
        Verifica se há ações para um match na tabela de fluxo, dado uma request.
        
        Args:
            request (list): Lista com as informações da request.
        
        Returns:
            list : Caso haja match, retorna a regra (lista de ações que devem ser executadas). Caso contrário, retorna False.
            
        """
        # Percorre a tabela de fluxo.
        for match in self._flow_table.copy():
            # Desconsidera e remove regras fechadas
            rule = self._flow_table[match][1]
            if not rule.opened:
                continue
            # Coleta as informações do match.
            bob, frange, neprs = match[0], match[1], match[2]
            # Se o bob da request for igual ao bob do match.
            if request.bob == bob:
                # Se o fmin da request estiver dentro do range de fidelidade do match.
                if (request.fmin >= frange[0]) and (request.fmin <= frange[1]):
                    # Se o número de pares EPR da request for menor ou igual ao número de pares EPR do match.
                    if request.neprs <= neprs:
                        return self._flow_table[match]
        return False
    
    def add_match_route_rule(self, bob, frange, neprs, route, rule):
        """
        Adiciona um match, rota e ação à tabela de fluxo.
            Args:
                bob (int): ID do host de destino.
                frange (tuple): Range de fidelidade a ser atendida para a comunicação.
                neprs (int): Número de pares EPR.
                route (list): Lista com a rota que a requisição deve seguir.
                rule (list): Lista com as ações que devem ser executadas.
        """
        # Inscreve a regra no gerenciador de tempo.
        time.subscribe_rule(rule)
        # Registra o host na regra.
        rule.set_host(self)
        # Adiciona o match, rota e regra à tabela de fluxo.
        match_flow = (bob, frange, neprs)
        self._flow_table[match_flow] = (route, rule)
        # Adiciona o index da regra ao dicionário de índices. Isso facilita a busca de regras na tabela de fluxo.
        self._rule_index[rule] = match_flow

    def find_match_by_rule(self, rule):
        """
        Encontra um match na tabela de fluxo dado uma regra.
        
        Args:
            rule (list): Lista de ações que devem ser executadas.
        """
        match_flow = self._rule_index[rule]
        return match_flow
    
    def remove_flow_by_rule(self, rule):
        """
        Deleta uma regra da tabela de fluxo.
        
        Args:
            rule (list): Lista de ações que devem ser executadas.
        """
        if rule not in self._rule_index:
            raise Exception('Regra não encontrada na tabela de fluxo.')
        # Encontra o match na tabela de fluxo.
        match_flow = self.find_match_by_rule(rule)
        del self._flow_table[match_flow]
        del self._rule_index[rule]
        
    
## Match fica na tabela de fluxo, são as chaves do dicionário.
## Request é o que chega, comparado ao match, são diferentes apenas pelo primeiro item. Que no request é o host_id do host que está enviando a requisição.
## Route é a rota que o pacote deve seguir.
# Actions são as ações que devem ser executadas. Especificamente classes. O controlador executará essas ações por meio da rede.
# rules são conjuntos de ações.