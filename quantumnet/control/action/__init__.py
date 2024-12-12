from importlib import import_module
from pkgutil import iter_modules
from sys import modules
from os import path
from .action import Action

# Define o diretório deste módulo
module_dir = path.dirname(__file__)

# Itera sobre todos os módulos no diretório
for _, module_name, _ in iter_modules([module_dir]):
    # Importa o módulo
    module = import_module(f".{module_name}", package=__name__)
    
    # Obtém todas as classes no módulo e as adiciona ao namespace do pacote
    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if isinstance(attr, type) and issubclass(attr, Action) and attr is not Action:
            setattr(modules[__name__], attr_name, attr)