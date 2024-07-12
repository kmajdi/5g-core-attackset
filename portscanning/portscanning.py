import subprocess
import time
from ..attack import Attack

class PortScanning(Attack):
    def __init__(self, target_ip, ports=["22", "80", "443"]):
        self.target_ip = target_ip
        self.ports = ports
        super.__init__("port_scanning")

    def execute(self, wait):
        time.sleep(wait)
        result = subprocess.run(['nmap', '-p', *self.ports, self.target_ip], capture_output=True, text=True)
        print(result.stdout)

    def get_log_start(self):
        return f"[{self.time_start}][{self.name}][{self.target_ip}] Attack Started"
    
    def get_log_end(self):
        self.finalize()
        return f"[{self.time_end}][{self.name}][{self.target_ip}] Attack Ended"
