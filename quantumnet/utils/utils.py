from random import uniform, randint
from quantumnet.objects.request import Request
# Registro
import csv
import os

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

# Função para registrar os dados no CSV
def register_request(request, estado_registro, filename="requests_data.csv"):
    """
    Registra as informações da request no CSV.
    
    Args:  
        request: objeto da request a ser registrada.
        estado_registro: se a request foi nova ou já tinha registro.
        filename: nome do arquivo CSV (padrão: "requests_data.csv").
    """
    # Verifica se o arquivo já existe para adicionar o cabeçalho se necessário
    file_exists = os.path.exists(filename)
    
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Se o arquivo não existe, adiciona o cabeçalho
        if not file_exists:
            writer.writerow(["ID", "Alice", "Bob", "Fidelidade Mínima", "Número de EPRs", "Início", "Término", "Novo Registro"])
        
        # Escreve os dados da request
        writer.writerow([str(request), request.alice, request.bob, request.fmin, request.neprs, request.starttime, request.endtime, estado_registro])