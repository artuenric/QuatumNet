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

def clear_file(filename):
    """
    Limpa o conteúdo de um arquivo CSV.

    Args:
        filename (str): Nome do arquivo CSV.
    """
    # Apaga o conteúdo do arquivo CSV
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        pass  # Não escreve nada, só abre e fecha o arquivo


# Função para registrar os dados no CSV
def register_request(request, estado_registro, filename):
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
            writer.writerow(["ID", "Alice", "Bob", "Fidelidade Minima", "Numero de EPRs", "Inicio", "Termino", "Novo Registro"])
        
        # Escreve os dados da request
        writer.writerow([str(request), request.alice, request.bob, request.fmin, request.neprs, request.starttime, request.endtime, estado_registro])

# Função para registrar o consumo de recursos
def register_consumption(time_slot, registry_of_resources, nome_arquivo):
    """
    Registra o número de qubits e pares EPR criados em um determinado time-slot em um arquivo CSV.

    Parâmetros:
    - time_slot (int): Time-slot atual.
    - registry_of_resources (dict): Dicionário com os recursos consumidos.
    - nome_arquivo (str): Nome do arquivo CSV de saída.
    """
    # Verifica se o arquivo já existe (cabeçalho só na primeira vez)
    try:
        with open(nome_arquivo, 'x', newline='') as arquivo_csv:
            escritor = csv.writer(arquivo_csv)
            escritor.writerow(['Time-Slot', 'Qubits Criados', 'Pares EPR Criados'])
    except FileExistsError:
        pass  # O arquivo já existe, não precisa reescrever o cabeçalho
    
    qubits_criados = registry_of_resources['qubits created']
    eprs_criados = registry_of_resources['eprs created']
    
    # Escreve os dados do time-slot atual
    with open(nome_arquivo, 'a', newline='') as arquivo_csv:
        escritor = csv.writer(arquivo_csv)
        escritor.writerow([time_slot, qubits_criados, eprs_criados])

    print(f"Time-slot {time_slot} registrado: Qubits = {qubits_criados}, EPRs = {eprs_criados}")
