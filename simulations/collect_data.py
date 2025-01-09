import csv
import os

def clear_file(file_path):
    """
    Limpa um arquivo CSV, removendo todos os dados.

    Args:
        file_path (str): Caminho para o arquivo CSV a ser limpo.
    """
    with open(file_path, 'w', newline='') as csvfile:
        csvfile.truncate()

def header_data_network(file_path):
    """
    Adiciona o cabeçalho a um arquivo CSV.

    Args:
        file_path (str): Caminho para o arquivo CSV.
    """
    header = [
        "time_slot",
        "qubits_active",
        "eprs_active",
        "qubits_created",
        "qubits_used",
        "eprs_created",
        "eprs_used",
        "rules_active"
    ]
    
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        with open(file_path, mode="w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)

def log_network(sim, filename, time):
    """
    Registra os dados de um time-slot no arquivo CSV.

    Parâmetros:
    - time_slot: índice do time-slot.
    - time: objeto que contém os dados do estado da simulação para o time-slot.
    """
    row = [
        time.get_current_time(),
        len(time.qubits),
        len(time.eprs),
        sim.network.registry_of_resources['qubits created'],
        sim.network.registry_of_resources['qubits used'],
        sim.network.registry_of_resources['eprs created'],
        sim.network.registry_of_resources['eprs used'],
        len(time.rules)
    ]
    
    # Adicionar a linha ao arquivo CSV
    with open(filename, mode="a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(row)

def log_request(filename, request, num_rule):
    """
    Registra as informações de uma única request em um arquivo CSV.

    Args:
        filename (str): Caminho para o arquivo CSV.
        request (Request): Objeto que contém as informações da request.
        num_rule (int): Número de regras ativas.
    """
    row = [
        request.id,
        request.starttime,
        request.endtime,
        request.endtime - request.starttime,
        num_rule
    ]
    # Adicionar a linha ao arquivo CSV
    with open(filename, mode="a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(row)

def header_data_requests(file_path):
    """
    Adiciona o cabeçalho a um arquivo CSV.

    Args:
        file_path (str): Caminho para o arquivo CSV.
    """
    header = [
        "id",
        "start_time",
        "end_time",
        "latency",
        "num_rules"
    ]
    
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        with open(file_path, mode="w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)