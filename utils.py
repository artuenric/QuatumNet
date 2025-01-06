from random import randint, uniform
from quantumnet.objects.request import Request
import csv

def generate_random_request(num_hosts, fmin_range, eprs_range):
    """
    Gera uma requisição aleatória com valores de fidelidade e número de EPRs aleatórios.

    Args:
        num_hosts (int): Número de hosts na rede.
        fmin_range (tuple): Intervalo de fidelidade mínima (mínimo, máximo).
        eprs_range (tuple): Intervalo de número de EPRs (mínimo, máximo).

    Returns:
        Request: Requisição gerada.
    """
    alice_id = randint(0, num_hosts - 1)
    bob_id = randint(0, num_hosts - 1)
    while bob_id == alice_id:
        bob_id = randint(0, num_hosts - 1)

    fmin = round(uniform(*fmin_range), 2)
    neprs = randint(*eprs_range)

    return Request(alice_id, bob_id, fmin, neprs)

def generate_random_traffic(num_hosts, n_requests, fmin_range=(0.5, 1.0), eprs_range=(1, 10)):
    """
    Gera uma lista de requisições aleatórias.

    Args:
        num_hosts (int): Número de hosts na rede.
        n_requests (int): Número de requisições a serem geradas.
        fmin_range (tuple): Intervalo de fidelidade mínima (mínimo, máximo).
        eprs_range (tuple): Intervalo de número de EPRs (mínimo, máximo).

    Returns:
        list: Lista de requisições geradas.
    """
    return [generate_random_request(num_hosts, fmin_range, eprs_range) for _ in range(n_requests)]

def generate_burst_traffic(num_hosts, requests_per_burst, n_bursts, fmin_range=(0.5, 1.0), eprs_range=(1, 10)):
    """
    Gera uma lista de requisições em rajadas.

    Args:
        num_hosts (int): Número de hosts na rede.
        requests_per_burst (int): Número de requisições por rajada.
        n_bursts (int): Número de rajadas a serem geradas.
        fmin_range (tuple): Intervalo de fidelidade mínima (mínimo, máximo).
        eprs_range (tuple): Intervalo de número de EPRs (mínimo, máximo).

    Returns:
        list: Lista de requisições geradas.
    """
    bursts = []
    for _ in range(n_bursts):
        burst_request = generate_random_request(num_hosts, fmin_range, eprs_range)
        bursts.extend([burst_request] * requests_per_burst)
    return bursts

def generate_mixed_traffic(num_hosts, n_requests, burst_probability=0.3, burst_size=5, fmin_range=(0.5, 1.0), eprs_range=(1, 10)):
    """
    Gera uma lista de requisições com rajadas intercaladas.

    Args:
        num_hosts (int): Número de hosts na rede.
        n_requests (int): Número de requisições a serem geradas.
        burst_probability (float): Probabilidade de gerar uma rajada.
        burst_size (int): Número de requisições por rajada.
        fmin_range (tuple): Intervalo de fidelidade mínima (mínimo, máximo).
        eprs_range (tuple): Intervalo de número de EPRs (mínimo, máximo).

    Returns:
        _type_: _description_
    """
    traffic = []
    for _ in range(n_requests):
        if uniform(0, 1) < burst_probability:
            burst_request = generate_random_request(num_hosts, fmin_range, eprs_range)
            traffic.extend([burst_request] * burst_size)
        else:
            traffic.append(generate_random_request(num_hosts, fmin_range, eprs_range))
    return traffic

def clear_file(file_path):
    """
    Limpa um arquivo CSV, removendo todos os dados.

    Args:
        file_path (str): Caminho para o arquivo CSV a ser limpo.
    """
    with open(file_path, 'w', newline='') as csvfile:
        csvfile.truncate()