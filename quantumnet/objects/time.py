class TimeManager:
    def __init__(self):
        self.current_time = 0

    def increment(self):
        """Increment the time-slot by 1."""
        self.current_time += 1

    def get_current_time(self):
        """Get the current time-slot."""
        return self.current_time

# Instância única do gerenciador de tempo
time = TimeManager()
