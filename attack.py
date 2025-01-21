from datetime import datetime, timedelta
import colorama
from colorama import Fore, Style

class Attack:
    def __init__(self, name):
        self.name = name
        self.time_start = datetime.now() - timedelta(hours=5)
        self.time_end = None

    def execute(self):
        pass
        
    def finalize(self):
        self.time_end = datetime.now() - timedelta(hours=5)

    def get_log_start(self):
        return f"{Fore.YELLOW}[{self.time_start}]{Fore.BLUE}[{self.name}]{Style.RESET_ALL} Attack Started"
    
    def get_log_end(self):
        self.finalize()
        return f"{Fore.YELLOW}[{self.time_start}]{Fore.BLUE}[{self.name}]{Style.RESET_ALL} Attack Started"
