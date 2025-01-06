def clear_file(file_path):
    """
    Limpa um arquivo CSV, removendo todos os dados.

    Args:
        file_path (str): Caminho para o arquivo CSV a ser limpo.
    """
    with open(file_path, 'w', newline='') as csvfile:
        csvfile.truncate()