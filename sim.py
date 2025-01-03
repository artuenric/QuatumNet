import random
from quantumnet.components import Controller, Network
from quantumnet.objects import time
from quantumnet.utils import *
from abc import ABC, abstractmethod

class Simulation(ABC):
    def __init__(self, info_network, info_controller, info_request, info_simulation):
        self.network = Network()
        self.controller = Controller(self.network)
        self.requests = []
        self.file_path = None
        # Processa as informações
        self.process_info_network(info_network)
        self.process_info_controller(info_controller)
        self.process_info_request(info_request)
        self.process_info_simulation(info_simulation)
        
    def process_info_network(self, info_network: dict):
        """
        Processa e atribui as informações da rede.
        """
        # Atribui os número de eprs e qubits iniciais na rede
        self.network.n_inital_eprs = info_network['n_initial_eprs']
        self.network.n_initial_qubits = info_network['n_initial_qubits']
        # Atribui a topologia da rede
        topology = info_network['topology_name']
        topology_params = info_network['topology_params']
        self.network.set_ready_topology(topology, topology_params)
    
    def process_info_controller(self, info_controller: dict):
        """
        Processa e atribui as informações do controlador.
        """
        # Atribui o TTL padrão para as regras
        self.controller.default_ttl = info_controller['default_ttl']
    
    def process_info_request(self, info_request: dict):
        """
        Processa e atribui as informações da requisição.
        """
        # Atribui o número de requisições a serem feitas
        self.n_requests = info_request['n_requests']
        # Atribui o range entre a fideliade mínima e máxima das requisições
        self.fidelity_requests_range = info_request['fidelity_requests_range']
        # Atribui o range entre o número de eprs das requisições
        self.n_eprs_requests_range = info_request['n_eprs_requests_range']
    
    def process_info_simulation(self, info_simulation: dict):
        """
        Processa e atribui as informações da simulação.
        """
        # Atribui o caminho do arquivo de saída
        self.file_path = info_simulation['file_path']
        # Atribui o periodo de tempo para reabastecer os recursos
        self.time_to_refill = info_simulation['time_to_refill']
        # Atribui o número de qubits a serem reabastecidos
        self.n_qubits_to_refill = info_simulation['n_qubits_to_refill']
        # Atribui o número de eprs a serem reabastecidos
        self.n_eprs_to_refill = info_simulation['n_eprs_to_refill']
    
    @abstractmethod
    def update_time(self):
        """
        Define o comportamento do tempo na simulação. Variando de acordo com a simulação.
        """
        pass
    
    @abstractmethod
    def run(self, n_steps):
        pass
    
    @abstractmethod
    def plot_results(self):
        pass

class RequestsHibridSimulation(Simulation):
    def __init__(self, info_network, info_controller, info_request, info_simulation):
        super().__init__(info_network, info_controller, info_request, info_simulation)
    
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
            if time.get_current_time() % self.time_to_refill == 0:
                self.network.refresh_resources(num_qubits=self.n_qubits_to_refill, num_eprs=self.n_eprs_to_refill)
                print(f"[Time {time.get_current_time()}] Recursos atualizados")
    
    def proactive_filling(self):
        """
        Preenche as tabelas de fluxo com regras de forma proativa.
        """
        hosts = self.network.hosts
        for alice in hosts:
            print(f"Adicionando regras para {alice}")
            for bob in hosts:
                self.controller.add_match_route_rule_in_host_proactive(alice, bob, (0.5, 0.6), 5)
                self.controller.add_match_route_rule_in_host_proactive(alice, bob, (0.8, 0.9), 5)
            # Mostra as tabelas
            self.network.get_host(alice).draw_flow_table()
    
    def process_requests_and_reactive_filling(self):
        for request in self.requests:
            print(f"[Time {time.get_current_time()}] Processando requisição {request}...")
            alice = self.network.get_host(request.alice)
            rule = alice.find_rule_by_request(request)

            if rule == False:  # Caso não exista um match na tabela
                request.starttime = time.get_current_time()
                self.update_time(3)
                self.controller.add_match_route_rule_in_host_reactive(request)
                rule = alice.find_rule_by_request(request)
                self.controller.run_rule(rule[1])
                request.endtime = time.get_current_time() 
                register_request(request, "Novo_Registro", self.file_path)
                
            else:  # Caso já exista a regra
                request.starttime = time.get_current_time()
                self.update_time(1)
                self.controller.run_rule(rule[1])
                request.endtime = time.get_current_time()
                register_request(request, "Ja_Registrado", self.file_path)
            
            # Exibir informações da requisição
            print(f"Request {request}: Start Time = {request.starttime}, End Time = {request.endtime}")

    def run(self, n_steps):
        """
        Executa a simulação.
        """
        # Limpa os arquivos de saída
        clear_file(self.file_path)
        
        # Preenche as tabelas de fluxo proativamente
        self.proactive_filling()
        
        # Cria n_requests requisições aleatórias
        for _ in range(self.n_requests):
            self.requests.append(generate_random_request(len(self.network.hosts), self.fidelity_requests_range, self.n_eprs_requests_range))
        
        # Percorre as requisições e preenche as tabelas de fluxo de forma reativa
        self.process_requests_and_reactive_filling()
    
    def plot_results(self):
        pass
    
class RequestsReactiveSimulation(Simulation):
    def __init__(self, info_network, info_controller, info_request, info_simulation):
        super().__init__(info_network, info_controller, info_request, info_simulation)
    
    def proactive_filling(self):
        """
        Preenche as tabelas de fluxo com regras de forma proativa.
        """
        hosts = self.network.hosts
        for alice in hosts:
            print(f"Adicionando regras para {alice}")
            for bob in hosts:
                self.controller.add_match_route_rule_in_host_proactive(alice, bob, (0.5, 0.6), 5)
                self.controller.add_match_route_rule_in_host_proactive(alice, bob, (0.8, 0.9), 5)
            # Mostra as tabelas
            self.network.get_host(alice).draw_flow_table()
    
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
            if time.get_current_time() % self.time_to_refill == 0:
                self.network.refresh_resources(num_qubits=self.n_qubits_to_refill, num_eprs=self.n_eprs_to_refill)
                print(f"[Time {time.get_current_time()}] Recursos atualizados")
        
    def process_requests(self, requests):
        """
        Processa as requisições de forma reativa.
        
        Args:
            requests (list): Lista de requisições a serem processadas.
        """
        
        for request in requests:
            print(f"[Time {time.get_current_time()}]")
            print(f"Request: {request}, Alice: {request.alice}, Bob: {request.bob}, Fmin: {request.fmin}, Neprs: {request.neprs}")
            alice = self.network.get_host(request.alice)
            rule = alice.find_rule_by_request(request)

            if rule == False:  # Caso não exista um match na tabela
                print(f"Descartando requisição {request} em {alice}")
                request.endtime = time.get_current_time()
                # Registra no CSV como um novo registro
                register_request(request, "Descartado", self.file_path)
                
            else:  # Caso já exista a regra
                request.starttime = time.get_current_time()
                self.controller.run_rule(rule[1])
                request.endtime = time.get_current_time() + 1        
                # Registra no CSV como já registrado
                register_request(request, "Já Registrado", self.file_path)
        
            self.update_time(1)
            # Exibir informações da requisição
            print(f"Request {request}: Start Time = {request.starttime}, End Time = {request.endtime}")
        
    def run(self):
        # Limpa os arquivos de saída
        clear_file(self.file_path)
        
        # Preenche as tabelas de fluxo proativamente
        self.proactive_filling()
        
        # Cria n_requests requisições aleatórias
        for _ in range(self.n_requests):
            self.requests.append(generate_random_request(len(self.network.hosts), self.fidelity_requests_range, self.n_eprs_requests_range))
        
        # Processa as requisições
        self.process_requests(self.requests)
    
    def plot_results(self):
        pass