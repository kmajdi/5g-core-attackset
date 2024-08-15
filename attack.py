import time

class Attack:
    def __init__(self, name):
        self.name = name
        self.time_start = time.time()
        self.time_end = None

    def execute(self):
        pass
        
    def finalize(self):
        self.time_end = time.time()

    def get_log_start(self):
        return f"[{self.time_start}][{self.name}] Attack Started"
    
    def get_log_end(self):
        self.finalize()
        return f"[{self.time_end}][{self.name}] Attack Ended"
