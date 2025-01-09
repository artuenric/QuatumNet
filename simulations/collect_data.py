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

def header(file_path):
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

def log(sim, time):
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
    with open(sim.filename, mode="a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(row)
