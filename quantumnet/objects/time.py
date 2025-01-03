class TimeManager:
    def __init__(self):
        self.current_time = 0
        self.qubits = []
        self.eprs = []
        self.rules = []

    def subscribe_qubit(self, qubit):
        """
        Inscreve um qubit no gerenciador de tempo.
        
        Args:
            qubit (Qubit): Qubit a ser inscrito.
        """
        self.qubits.append(qubit)
    
    def subscribe_epr(self, epr):
        """
        Inscreve um par EPR no gerenciador de tempo.

        Args:
            epr (EPR): Par EPR a ser inscrito.
        """
        self.eprs.append(epr)
    
    def subscribe_rule(self, rule):
        """
        Inscreve uma regra no gerenciador de tempo.

        Args:
            rule (Rule): Regra a ser inscrita.
        """
        self.rules.append(rule)
    
    def notify_qubits(self):
        """Notifica aos qubits a passsagem de tempo."""
        for qubit in self.qubits:
            qubit.update_time(self.current_time)
    
    def notify_eprs(self):
        """Notifica aos pares EPR a passagem de tempo."""
        for epr in self.eprs:
            epr.update_time(self.current_time)
    
    def notify_rules(self):
        """Notifica as regras a passagem de tempo."""
        for rule in self.rules:
            rule.update_time()
            
    def increment(self):
        """Increment the time-slot by 1."""
        self.current_time += 1
        self.notify_qubits()
        self.notify_eprs()
        self.notify_rules()

    def get_current_time(self):
        """Get the current time-slot."""
        return self.current_time

# Instância única do gerenciador de tempo
time = TimeManager()
