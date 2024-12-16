from random import uniform, randint
from quantumnet.objects.request import Request

def generate_random_request(num_hosts, fmin_range=(0.5, 1.0), eprs_range=(1, 10)):
    """
    Gera uma request aleatória para a rede quântica.

    Args:
        num_hosts (int): Número total de hosts na rede.
        fmin_range (tuple): Intervalo para o valor mínimo de fidelidade (fmin).
        eprs_range (tuple): Intervalo para o número de pares EPR requeridos.

    Returns:
        list: Uma request no formato [alice_id, bob_id, fmin, eprs].
    """
    alice_id = randint(0, num_hosts - 1)
    bob_id = randint(0, num_hosts - 1)

    # Garantir que Alice e Bob não sejam o mesmo host
    while bob_id == alice_id:
        bob_id = randint(0, num_hosts - 1)

    fmin = round(uniform(*fmin_range), 2)  
    neprs = randint(*eprs_range)            

    return Request(alice_id, bob_id, fmin, neprs)