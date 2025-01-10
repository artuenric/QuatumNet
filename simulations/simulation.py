from quantumnet.components import Network, Controller
from .generate_requests import generate_traffic
from .collect_data import *
import random
from quantumnet.objects import time, logger

class Sim():
    def __init__(self, network_info, controller_info):
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
        self.requests =  None
    
    def set_file_data_network(self, filename):
        default_path = 'resultados/analise_rede/'
        self.filename = default_path + filename
        # Limpa o arquivo
        clear_file(self.filename)
        # Adiciona o cabeçalho
        header_data_network(self.filename)
    
    def set_file_data_requests(self, filename):
        default_path = 'resultados/analise_requests/'
        self.filename_requests = default_path + filename
        # Limpa o arquivo
        clear_file(self.filename_requests)
        # Adiciona o cabeçalho
        header_data_requests(self.filename_requests)
    
    def set_requests(self, requests):
        self.requests = requests
    
    def app(self, request):
        """
        Consome o par EPR fim a fim.

        Args:
            request (_type_): _description_
        """
        # Obtém o par EPR fim a fim
        eprs_e2e = self.controller.network.get_eprs_from_edge(request.alice, request.bob)
        if eprs_e2e == False or len(eprs_e2e) == 0:
            return False
        # Consome o par EPR
        epr = eprs_e2e[0]
        self.controller.network.physicallayer.remove_epr_from_channel(epr, epr.channel)
        
    def proactive_filling(self, proactive_params):
        """
        Preenhce as tabelas de forma proativa.
        """
        # Preenche as tabelas de forma proativa
        for alice in self.network.hosts:
            logger.debug(f"Adicionando regras para {alice}")
            for bob in self.network.hosts:
                for key in proactive_params.keys():
                    self.controller.add_match_route_rule_in_host_proactive(alice, bob, proactive_params[key]['frange'], proactive_params[key]['neprs'])
    
    def hibrid_initial_filling(self, proactive_params):
        """
        Preenhce as tabelas de forma proativa.
        """
        # Preenche as tabelas de forma proativa
        for alice in self.network.hosts:
            logger.debug(f"Adicionando regras para {alice}")
            for bob in self.network.hosts:
                if random.uniform(0, 1) < 0.5:
                    for key in proactive_params.keys():
                        self.controller.add_match_route_rule_in_host_proactive(alice, bob, proactive_params[key]['frange'], proactive_params[key]['neprs'])
        
    def proactive_process_requests(self):
        # Processa as requisições
        for request in self.requests:
            logger.debug(f"[Time {time.get_current_time()}] Processando requisição {request}...")
            alice = self.network.get_host(request.alice)
            rule = alice.find_rule_by_request(request)

            if rule == False:  # Caso não exista um match na tabela
                logger.debug(f"[Time {time.get_current_time()}] Descartando requisição {request} no Host {alice}.")
                # Finaliza a requisição descartada
                request.starttime = time.get_current_time()
                request.endtime = time.get_current_time()
                # Registra a requisição descartada
                self.controller.fulfill_request(request)
                
            else:  # Caso já exista a regra
                logger.debug(f"[Time {time.get_current_time()}] Atendendo requisição {request} no Host {alice}.")
                request.starttime = time.get_current_time()
                # Executa a regra n vezes (neprs)
                for i in range(request.neprs):
                    self.controller.run_rule(rule[1])
                # Finaliza a requisição atendida
                request.endtime = time.get_current_time() + 1
                request.completed = True     
                # Registra a requisição atendida
                self.controller.successful_request(request)
                # Exibir informações da requisição
                logger.debug(f"Request {request}: Start Time = {request.starttime}, End Time = {request.endtime}")
            
            # Registra a requisição
            log_request(self.filename_requests, request, len(time.rules))
            
            # App
            self.app(request)
            
            # Atualiza o tempo
            self.update_time(1)
    
    def reactive_process_requests(self):
        for request in self.requests:
            logger.debug(f"[Time {time.get_current_time()}] Processando requisição {request}...")
            alice = self.network.get_host(request.alice)
            rule = alice.find_rule_by_request(request)

            if rule == False:  # Caso não exista um match na tabela
                request.starttime = time.get_current_time()
                self.update_time(3)
                logger.debug(f"[Time {time.get_current_time()}] Adicionando regra no Host {alice}")
                self.controller.add_match_route_rule_in_host_reactive(request)
                rule = alice.find_rule_by_request(request)
                
            else:  # Caso já exista a regra
                logger.debug(f"[Time {time.get_current_time()}] Regra existente para {request} no Host {alice}.")
                request.starttime = time.get_current_time()
                self.update_time(1)
                    
            # Executa a regra
            logger.debug(f"[Time {time.get_current_time()}] Atendendo requisição {request} no Host {alice}.")
            for i in range(request.neprs):
                self.controller.run_rule(rule[1])
            request.endtime = time.get_current_time()
            
            # Consome o par EPR
            self.app(request)
            
            # Registra a requisição atendida
            self.controller.successful_request(request)
            request.completed = True
            
            # Registra a requisição
            log_request(self.filename_requests, request, len(time.rules))
            
            # Exibir informações da requisição
            logger.debug(f"[Time {time.get_current_time()}] Request {request}: Start Time = {request.starttime}, End Time = {request.endtime}")

            
    def update_time(self, n_time_slots):
        """
        Atualiza o tempo e as regras

        Args:
            time_for_update (int): Tempo para incrementar o time-slot.
        """
        # Atualiza o tempo
        for t in range(n_time_slots):
            log_network(self, self.filename, time)
            time.increment()
            # Atualiza os recursos de 10 em 10
            if time.get_current_time() % self.time_to_refill== 0:
                self.network.refresh_resources(num_qubits=self.network.n_initial_qubits, num_eprs=self.network.n_initial_eprs)
                logger.debug(f"[Time {time.get_current_time()}] Recursos atualizados")
            
    
    def end(self):
        time.reset()