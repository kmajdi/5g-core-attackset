import subprocess
import time

class PortScanning:
    def __init__(self, target_ip):
        self.target_ip = target_ip

    def attack(self, wait):
        time.sleep(wait)
        result = subprocess.run(['nmap', '-p', "22", "80", "443", self.target_ip], capture_output=True, text=True)
        print(result.stdout)

    def clean_up(self, wait):
        time.sleep(wait)
        print("No cleanup required for Port Scanning")

# Example usage for AMF component:
def get_ips():
    result = subprocess.run("kubectl get services --all-namespaces".split(), capture_output=True, text=True)
    output = [h for h in result.stdout.strip().split() if h.startswith("10.")]
    return output

for h in get_ips():
    port_scanning_amf = PortScanning(h)
    port_scanning_amf.attack(0)
