from random import randint, uniform
from quantumnet.objects.request import Request
import copy

def generate_random_traffic(num_hosts, n_requests, fmin_range, eprs_range):
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
    requests = []
    for _ in range(n_requests):
        alice_id = randint(0, num_hosts - 1)
        bob_id = randint(0, num_hosts - 1)
        while bob_id == alice_id:
            bob_id = randint(0, num_hosts - 1)

        fmin = round(uniform(*fmin_range), 2)
        neprs = randint(*eprs_range)
        requests.append(Request(alice_id, bob_id, fmin, neprs))
    return requests

def generate_burst_traffic(num_hosts, n_requests, fmin_range, eprs_range):
    """
    Gera uma lista de requisições em rajadas.

    Args:
        num_hosts (int): Número de hosts na rede.
        n_requests (int): Número de requisições a serem geradas.
        fmin_range (tuple): Intervalo de fidelidade mínima (mínimo, máximo).
        eprs_range (tuple): Intervalo de número de EPRs (mínimo, máximo).

    Returns:
        list: Lista de requisições geradas.
    """
    requests = []
    requests_per_burst = max(1, n_requests // 5)
    for _ in range(n_requests // requests_per_burst):
        alice_id = randint(0, num_hosts - 1)
        bob_id = randint(0, num_hosts - 1)
        while bob_id == alice_id:
            bob_id = randint(0, num_hosts - 1)

        fmin = round(uniform(*fmin_range), 2)
        neprs = randint(*eprs_range)
        base_request = Request(alice_id, bob_id, fmin, neprs)

        requests.extend([copy.deepcopy(base_request) for _ in range(requests_per_burst)])

    while len(requests) > n_requests:
        requests.pop()

    return requests

def generate_mixed_traffic(num_hosts, n_requests, burst_probability, burst_size, fmin_range, eprs_range):
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
        list: Lista de requisições geradas.
    """
    requests = []
    while len(requests) < n_requests:
        if uniform(0, 1) < burst_probability:
            alice_id = randint(0, num_hosts - 1)
            bob_id = randint(0, num_hosts - 1)
            while bob_id == alice_id:
                bob_id = randint(0, num_hosts - 1)

            fmin = round(uniform(*fmin_range), 2)
            neprs = randint(*eprs_range)
            burst_request = Request(alice_id, bob_id, fmin, neprs)

            requests.extend([copy.deepcopy(burst_request) for _ in range(burst_size)])
        else:
            alice_id = randint(0, num_hosts - 1)
            bob_id = randint(0, num_hosts - 1)
            while bob_id == alice_id:
                bob_id = randint(0, num_hosts - 1)

            fmin = round(uniform(*fmin_range), 2)
            neprs = randint(*eprs_range)
            requests.append(Request(alice_id, bob_id, fmin, neprs))

    return requests[:n_requests]

def generate_traffic(request_params):
    """
    Gera uma lista de requisições com base no tipo de tráfego especificado.

    Args:
        request_params (dict): Dicionário contendo informações sobre o tráfego.
            - traffic_type (str): Tipo de tráfego a ser gerado ('random', 'burst', 'mixed').
            - burst_probability (float): Probabilidade de gerar uma rajada (usado apenas para tráfego 'mixed').
            - burst_size (int): Número de requisições por rajada (usado apenas para tráfego 'mixed').
            - fmin_range (tuple): Intervalo de fidelidade mínima (mínimo, máximo).
            - eprs_range (tuple): Intervalo de número de EPRs (mínimo, máximo).
            - num_hosts (int): Número de hosts na rede.
            - n_requests (int): Número de requisições a serem geradas.

    Returns:
        list: Lista de requisições geradas.
    """
    num_hosts = request_params.get('num_hosts')
    n_requests = request_params.get('n_requests')
    traffic_type = request_params.get('traffic_type')
    fmin_range = request_params.get('fmin_range', (0.5, 1.0))
    eprs_range = request_params.get('eprs_range', (1, 10))

    if traffic_type == 'random':
        return generate_random_traffic(num_hosts, n_requests, fmin_range, eprs_range)
    elif traffic_type == 'burst':
        return generate_burst_traffic(num_hosts, n_requests, fmin_range, eprs_range)
    elif traffic_type == 'mixed':
        burst_probability = request_params.get('burst_probability', 0.3)
        burst_size = request_params.get('burst_size', 5)
        return generate_mixed_traffic(num_hosts, n_requests, burst_probability, burst_size, fmin_range, eprs_range)
    else:
        raise ValueError("Tipo de tráfego inválido. Escolha entre 'random', 'burst' ou 'mixed'.")
