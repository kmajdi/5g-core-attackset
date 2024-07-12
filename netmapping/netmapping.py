import subprocess
import time
from ..attack import Attack

class NetworkMapping(Attack):
    def __init__(self, target_ip):
        self.target_ip = target_ip
        super().__init__("net_mapping")

    def execute(self, wait):
        time.sleep(wait)
        result = subprocess.run(['nmap', self.target_ip], capture_output=True, text=True)
        print(result.stdout)

    def clean_up(self, wait):
        time.sleep(wait)
        print("No cleanup required for Network Mapping")
        
    def get_log_start(self):
        return f"[{self.time_start}][{self.name}][{self.target_ip}] Attack Started"
    
    def get_log_end(self):
        self.finalize()
        return f"[{self.time_end}][{self.name}][{self.target_ip}] Attack Ended"