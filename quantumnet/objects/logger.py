import logging
from . import time
class Logger:
    _instance = None  # Singleton
    DISABLED = False

    def __new__(cls):
        if cls._instance is None:
            instance = super().__new__(cls)
            instance.logger = logging.getLogger('qkdnet')
            instance.logger.setLevel(logging.DEBUG)  # Nível padrão
            # Configurando o handler com formato
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            instance.logger.addHandler(handler)
            instance.logger.propagate = False  # Evita logs duplicados
            cls._instance = instance
        return cls._instance

    @staticmethod
    def activate():
        Logger.DISABLED = False

    @staticmethod
    def deactivate():
        Logger.DISABLED = True

    def set_level(self, level):
        """
        Define o nível mínimo de log a ser exibido.
        Níveis possíveis: DEBUG, INFO, WARNING, ERROR, CRITICAL
        """
        self.logger.setLevel(level)

    def log(self, level, message):
        if not Logger.DISABLED:
            self.logger.log(level, message)

    def debug(self, message):
        self.log(logging.DEBUG, message)

    def info(self, message):
        self.log(logging.INFO, message)

    def warn(self, message):
        self.log(logging.WARNING, message)

    def error(self, message):
        self.log(logging.ERROR, message)

    def critical(self, message):
        self.log(logging.CRITICAL, message)

# Instância do logger
logger = Logger()