import subprocess
import time

class NetworkMapping:
    def __init__(self, target_ip):
        self.target_ip = target_ip

    def attack(self, wait):
        time.sleep(wait)
        result = subprocess.run(['nmap', self.target_ip], capture_output=True, text=True)
        print(result.stdout)

    def clean_up(self, wait):
        time.sleep(wait)
        print("No cleanup required for Network Mapping")

def get_ips():
    result = subprocess.run("kubectl get services --all-namespaces".split(), capture_output=True, text=True)
    output = [h for h in result.stdout.strip().split() if h.startswith("10.")]
    return output

for h in get_ips():
    network_mapping_amf = NetworkMapping(h)
    network_mapping_amf.attack(0)
